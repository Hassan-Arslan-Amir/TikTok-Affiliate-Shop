import wx
import wx.dataview as dv
from db_utils import update_last_modified, get_products_by_shop, add_product, update_product_enabled, get_connection, delete_product
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class ProductsDialog(wx.Dialog):
    def __init__(self, parent, shop_id):
        super().__init__(parent, title="Manage Products", size=(700, 500))
        self.shop_id = shop_id
        self.editing_productid = None

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        # Top: Add new product section (30%)
        top_panel = wx.Panel(self)
        top_panel.SetBackgroundColour(wx.Colour(250, 250, 250))
        top_sizer = wx.BoxSizer(wx.VERTICAL)

        font_label = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        label = wx.StaticText(top_panel, label="Add new products")
        label.SetFont(font_label)
        top_sizer.Add(label, 0, wx.ALL, 10)

        # Horizontal box for productid and commission combo separated by a line
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.product_id_txt = wx.TextCtrl(top_panel)
        self.product_id_txt.SetHint("Enter Product ID")
        self.product_id_txt.SetBackgroundColour(wx.Colour(245, 245, 245))
        self.product_id_txt.SetForegroundColour(wx.Colour(0, 0, 0))
        self.product_id_txt.SetWindowStyle(wx.BORDER_SIMPLE)
        hbox.Add(self.product_id_txt, 1, wx.EXPAND | wx.ALL, 5)

        line = wx.StaticLine(top_panel, style=wx.LI_VERTICAL)
        hbox.Add(line, 0, wx.EXPAND | wx.ALL, 5)

        # self.commission_cb = wx.ComboBox(top_panel, style=wx.CB_READONLY)
        # self.commission_cb.AppendItems([f"{i}%" for i in range(0, 101, 5)])
        # self.commission_cb.SetSelection(0)
        # self.commission_cb.SetBackgroundColour(wx.Colour(245, 245, 245))
        # self.commission_cb.SetForegroundColour(wx.Colour(0, 0, 0))
        # hbox.Add(self.commission_cb, 1, wx.EXPAND | wx.ALL, 5)
        self.commission_cb = wx.TextCtrl(top_panel)
        self.commission_cb.SetHint("Enter commission rate")
        self.commission_cb.SetBackgroundColour(wx.Colour(245, 245, 245))
        self.commission_cb.SetForegroundColour(wx.Colour(0, 0, 0))
        self.commission_cb.SetWindowStyle(wx.BORDER_SIMPLE)
        hbox.Add(self.commission_cb, 1, wx.EXPAND | wx.ALL, 5)

        top_sizer.Add(hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        # Add Product button aligned bottom right
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.AddStretchSpacer(1)
        add_btn = wx.Button(top_panel, label="Add Product")
        add_btn.Bind(wx.EVT_BUTTON, self.on_add_or_update_product)
        add_btn.SetBackgroundColour(wx.Colour(65, 105, 225))
        add_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        btn_sizer.Add(add_btn, 0, wx.ALL, 10)
        top_sizer.Add(btn_sizer, 0, wx.EXPAND)

        top_panel.SetSizer(top_sizer)
        main_sizer.Add(top_panel, 0, wx.EXPAND | wx.ALL, 5)
        # Horizontal separator line
        separator_line = wx.StaticLine(self)
        main_sizer.Add(separator_line, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        # Bottom: Products list section (70%)
        bottom_panel = wx.Panel(self)
        bottom_panel.SetBackgroundColour(wx.Colour(245, 245, 245))
        bottom_sizer = wx.BoxSizer(wx.VERTICAL)

        label2 = wx.StaticText(bottom_panel, label="My Products")
        label2.SetFont(font_label)
        bottom_sizer.Add(label2, 0, wx.ALL, 10)

        # DataViewListCtrl for products table
        self.dvlc = dv.DataViewListCtrl(bottom_panel, style=wx.dataview.DV_ROW_LINES | wx.dataview.DV_VERT_RULES)
        self.dvlc.AppendTextColumn("Index", width=50)
        self.dvlc.AppendTextColumn("Product ID", width=150)
        self.dvlc.AppendTextColumn("Commission", width=100)
        self.dvlc.AppendTextColumn("Enabled", width=70)

        orig_edit_img = wx.Image(resource_path("icons/edit.png"), wx.BITMAP_TYPE_PNG)
        scaled_edit_img = orig_edit_img.Scale(20, 20, wx.IMAGE_QUALITY_HIGH)
        self.edit_bmp = wx.Bitmap(scaled_edit_img)

        orig_delete_img = wx.Image(resource_path("icons/delete.png"), wx.BITMAP_TYPE_PNG)
        scaled_delete_img = orig_delete_img.Scale(20, 20, wx.IMAGE_QUALITY_HIGH)
        self.delete_bmp = wx.Bitmap(scaled_delete_img)

        # Add icon columns
        self.edit_renderer = dv.DataViewBitmapRenderer()
        self.edit_col = dv.DataViewColumn("Edit", self.edit_renderer, 4, width=40)
        self.dvlc.AppendColumn(self.edit_col)

        self.delete_renderer = dv.DataViewBitmapRenderer()
        self.delete_col = dv.DataViewColumn("Delete", self.delete_renderer, 5, width=40)
        self.dvlc.AppendColumn(self.delete_col)

        bottom_sizer.Add(self.dvlc, 1, wx.EXPAND | wx.ALL, 5)

        self.dvlc.Bind(dv.EVT_DATAVIEW_ITEM_ACTIVATED, self.on_item_activated)
        
        # Done button aligned bottom right
        done_sizer = wx.BoxSizer(wx.HORIZONTAL)
        done_sizer.AddStretchSpacer(1)
        done_btn = wx.Button(bottom_panel, label="Done")
        done_btn.Bind(wx.EVT_BUTTON, self.on_done)
        done_btn.SetBackgroundColour(wx.Colour(65, 105, 225))
        done_btn.SetForegroundColour(wx.Colour(255, 255, 255))       
        done_sizer.Add(done_btn, 0, wx.ALL, 10)
        bottom_sizer.Add(done_sizer, 0, wx.EXPAND)

        bottom_panel.SetSizer(bottom_sizer)
        main_sizer.Add(bottom_panel, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_sizer)

        self.load_products()

    def load_products(self):
        self.dvlc.DeleteAllItems()
        products = get_products_by_shop(self.shop_id)
        print("Loaded products:", products)
        for idx, p in enumerate(products, start=1):
            enabled = "✓" if p["enabled"] else "✗"
            self.dvlc.AppendItem([
                str(idx), 
                p["productid"], 
                p["commission"], 
                enabled,
                self.edit_bmp, 
                self.delete_bmp
                ])

    def on_add_or_update_product(self, event):
        productid = self.product_id_txt.GetValue().strip()
        commission = self.commission_cb.GetValue().strip()
        if commission and not commission.endswith('%'):
            commission += '%'
        if not productid:
            wx.MessageBox("Please enter a Product ID.", "Error", wx.OK | wx.ICON_ERROR)
            return

        if self.editing_productid:  # Update existing product
            update_product_enabled(self.shop_id, self.editing_productid, 1)  # keep enabled by default
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "UPDATE products SET productid = ?, commission = ? WHERE shop_id = ? AND productid = ?",
                (productid, commission, self.shop_id, self.editing_productid)
            )
            conn.commit()
            wx.MessageBox(f"Product '{self.editing_productid}' updated.", "Info", wx.OK | wx.ICON_INFORMATION)
            self.load_products()
            self.editing_productid = None
        else:  # Add new product
            add_product(self.shop_id, productid, commission, enabled=1)
            wx.MessageBox(f"Product '{productid}' added.", "Info", wx.OK | wx.ICON_INFORMATION)
            self.load_products()

        self.product_id_txt.SetValue("")
        self.commission_cb.SetValue("")
        

    def on_item_activated(self, event):
        print("Item activated")
        row = self.dvlc.ItemToRow(event.GetItem())
        col = event.GetColumn()
        # Only toggle if Enabled column clicked (index 3)
        if col == 3:
            productid = self.dvlc.GetTextValue(row, 1)
            current_val = self.dvlc.GetTextValue(row, 3)
            new_enabled = 0 if current_val == "✓" else 1
            update_product_enabled(self.shop_id, productid, new_enabled)
            self.load_products() 
        if col == 4:
            productid = self.dvlc.GetTextValue(row, 1)
            commission = self.dvlc.GetTextValue(row, 2)

            self.product_id_txt.SetValue(productid)
            self.commission_cb.SetValue(commission)
            self.editing_productid = productid
            #self.add_btn.SetLabel("Update Product")
        elif col == 5:
            productid = self.dvlc.GetTextValue(row, 1)
            dlg = wx.MessageDialog(self, f"Are you sure you want to delete product '{productid}'?", "Confirm Delete", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING)
            if dlg.ShowModal() == wx.ID_YES:
                delete_product(self.shop_id, productid)
                wx.MessageBox(f"Product '{productid}' deleted.", "Info", wx.OK | wx.ICON_INFORMATION)
                self.load_products()
            dlg.Destroy()    

    def on_done(self, event):
        update_last_modified(self.shop_id)
        self.EndModal(wx.ID_OK)
