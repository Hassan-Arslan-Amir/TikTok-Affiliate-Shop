import wx
import uuid
import os
import re
from db_utils import fetch_shops, insert_shop, update_shop, delete_shop, init_db, save_upload,insert_cookie,reset_tables, alter_table, debug_print_uploads, print_table_columns, get_user_names
import wx.lib.buttons as button
from uploadfile import UploadDialog
from products_dialog import ProductsDialog
from Tiktok_Bot_merge import runner
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def safe_bitmap(path, fallback_art=wx.ART_MISSING_IMAGE, size=(24, 24)):
    """Safely loads a bitmap from file or falls back to a default icon."""
    try:
        if os.path.exists(path):
            img = wx.Image(path, wx.BITMAP_TYPE_ANY)
            img = img.Scale(size[0], size[1], wx.IMAGE_QUALITY_HIGH)
            return wx.Bitmap(img)
        else:
            print(f"[safe_bitmap] File not found: {path}, using fallback.")
    except Exception as e:
        print(f"[safe_bitmap] Error loading bitmap from {path}: {e}")
    
    # Use built-in fallback if anything fails
    return wx.ArtProvider.GetBitmap(fallback_art, wx.ART_TOOLBAR, size)

class ShopPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        #reset_tables(['users', 'uploads', 'cookies', 'shops', 'products'])
        #alter_table()
        #names = get_user_names()
        #print(names)
        init_db()
        #print_table_columns("shops")
        self.shops_data = []

        self.SetBackgroundColour(wx.Colour(245, 245, 245))
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Top Navigation Bar Panel (Black Background)
        nav_panel = wx.Panel(self, size=(-1, 60))
        nav_panel.SetBackgroundColour(wx.Colour(0, 0, 0))
        nav_sizer = wx.BoxSizer(wx.HORIZONTAL)
        nav_panel.SetSizer(nav_sizer)

        # TikTok Shop title on the left
        title = wx.StaticText(nav_panel, label="TikTok Shop")
        title.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour(wx.WHITE)
        nav_sizer.Add(title, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 20)

        nav_sizer.AddStretchSpacer(1)

        # Navigation buttons on the right
        for label, handler in [
            ("Home", self.go_to_home),
            ("Add a Shop", self.show_add_shop_popup),
            ("Reports", self.go_to_reporting)
        ]:
            btn = self.create_nav_button(nav_panel, label, handler)
            btn.SetBackgroundColour(wx.Colour(0,0,0))  # Dark gray to match navbar
            btn.SetForegroundColour(wx.WHITE)
            nav_sizer.Add(btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)

        main_sizer.Add(nav_panel, 0, wx.EXPAND | wx.Top, 0)

        self.shop_list_panel = ShopListPanel(self)
        main_sizer.Add(self.shop_list_panel, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(main_sizer)

        self.load_shops_from_db()

    def create_nav_button(self,parent, label, handler):
        btn = button.GenButton(parent, label=label, size=(130, 40))
        #btn.SetBackgroundColour(wx.Colour(65, 105, 225))
        btn.SetForegroundColour(wx.WHITE)
        btn.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        btn.Bind(wx.EVT_BUTTON, handler)
        btn.SetWindowStyleFlag(wx.BORDER_NONE)
        return btn

    def go_to_home(self, event):
        from home_panel import HomePanel
        self.GetParent().switch_panel(HomePanel)

    def go_to_reporting(self, event):
        from reporting_panel import ReportingPanel
        self.GetParent().switch_panel(ReportingPanel)

    def show_add_shop_popup(self, event):
        from add_shop_dialog import AddShopDialog
        dialog = AddShopDialog(self)
        if dialog.ShowModal() == wx.ID_OK:
            values = dialog.get_values()
            shop_id = str(uuid.uuid4())
            insert_shop(shop_id, values["Name"], values["ShopType"], values["Email"],
                        values["Phone Number"], values["Message"], 
                        values.get("Follow-up Message", ""), values["Valid Until"])
            wx.CallAfter(self.load_shops_from_db)
        dialog.Destroy()

    def on_edit(self, card, current_name, current_type):
        from add_shop_dialog import AddShopDialog
        from db_utils import update_last_modified
        shop = next((s for s in self.shops_data if s["name"] == current_name and s["type"] == current_type), None)
        if not shop:
            wx.MessageBox("Shop not found!", "Error", wx.OK | wx.ICON_ERROR)
            return

        dialog = AddShopDialog(self, shop_data=shop)
        if dialog.ShowModal() == wx.ID_OK:
            values = dialog.get_values()
            shop.update({
                "name": values["Name"],
                "type": values["ShopType"],
                "email": values["Email"],
                "phone": values["Phone Number"],
                "message": values["Message"],
                "followup": values.get("Follow-up Message",""),
                "validdate":values["Valid Until"]
            })
            update_shop(shop)
                # Update filename in uploads table if filename changed or provided
            if "filename" in shop and shop["filename"]:
                save_upload(shop["id"], shop["filename"], shop.get("filepath", ""))

            update_last_modified(shop["id"])
            wx.CallAfter(self.load_shops_from_db)
        dialog.Destroy()

    def on_delete(self, card, shop_id):
        confirm = wx.MessageDialog(self, "Are you sure you want to delete?", "Confirm Delete",
                                   wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING)
        if confirm.ShowModal() == wx.ID_YES:
            delete_shop(shop_id)
            wx.CallAfter(self.load_shops_from_db)
        confirm.Destroy()

    def toggle_start_stop(self, event, btn, status_label, shop_name, card):
            log_box = getattr(card, "log_box", None)
            def log_callback(msg):
                if log_box:
                    wx.CallAfter(log_box.AppendText, msg + "\n")

            button = event.GetEventObject()
            if button.GetLabel() == "Start":
                if log_box:
                    log_box.SetValue("")       
                    log_box.Show()           
                    card.Layout()
                runner.start(shop_name, log_callback=log_callback)
                button.SetLabel("Stop")
                button.SetBackgroundColour(wx.Colour(220, 20, 60))
                status_label.SetLabel("Started")
                status_label.SetForegroundColour(wx.Colour(34, 139, 34))
                button.SetForegroundColour(wx.WHITE)
            else:
                runner.stop()
                if log_box:
                    log_box.Hide()
                    card.Layout()
                button.SetLabel("Start")
                button.SetBackgroundColour(wx.Colour(65, 105, 225))
                status_label.SetLabel("Stopped")
                status_label.SetForegroundColour(wx.Colour(178, 34, 34))   
                button.SetForegroundColour(wx.WHITE)
                wx.CallAfter(self.load_shops_from_db)

    def on_cookies(self, shop_id, name):
        dialog = wx.Dialog(self, title=f"Cookies for {name}", size=(700, 500))
        dialog.Center()
        panel = wx.Panel(dialog)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Label
        label = wx.StaticText(panel, label="Enter json file:")
        vbox.Add(label, flag=wx.ALL | wx.EXPAND, border=10)

        # Text input
        cookies_text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        vbox.Add(cookies_text_ctrl, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=10)

        # Attach button
        attach_btn = wx.Button(panel, label="Attach")
        vbox.Add(attach_btn, flag=wx.ALL | wx.ALIGN_CENTER, border=10)

        panel.SetSizer(vbox)

        def on_attach(event):
            cookie_text = cookies_text_ctrl.GetValue().strip()
            if not cookie_text:
                wx.MessageBox("Please enter some text before attaching.", "Warning", wx.OK | wx.ICON_WARNING)
                return
            # print(f"Attaching cookie for shop_id={shop_id}: {cookie_text}")  # Terminal log

            success = insert_cookie(shop_id, cookie_text)
            print("Insert cookie result:", success)
            if success:
                from db_utils import update_last_modified
                update_last_modified(shop_id)
                wx.MessageBox("Cookie attached successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
                wx.CallAfter(self.load_shops_from_db)
                dialog.Close()
            else:
                wx.MessageBox("Failed to attach cookie. Check logs.", "Error", wx.OK | wx.ICON_ERROR)

        attach_btn.Bind(wx.EVT_BUTTON, on_attach)
        dialog.ShowModal()
        dialog.Destroy()

    def on_upload(self, event, shop_id):
        dlg = UploadDialog(self, shop_id)
        dlg.Center()
        if dlg.ShowModal() == wx.ID_OK:
            print("Selected file inside on_upload after ShowModal():", dlg.selected_file) 
            filepath = dlg.selected_file
            filename = os.path.basename(filepath)
            print("filename:", filename, "filepath:", filepath)  
            save_upload(shop_id, filename, filepath)
            #debug_print_uploads()
            wx.CallAfter(self.load_shops_from_db)
        dlg.Destroy()

    def on_products(self, event, sid):
        dlg = ProductsDialog(self, sid)
        dlg.ShowModal()
        dlg.Destroy()
        # After dialog closes, reload shops or update card UI
        wx.CallAfter(self.load_shops_from_db)

    def add_shop_card(self, id, name, type, email="", phone="", message="", followup="",productid="" ,filename=None, filepath=None, last_modified="",commission="", validdate="", count=""):
        COUNTRY_MAP = {
            "+1": "USA",
            "+44": "UK",
            "+49": "Germany"
        }
        def hover_effect(btn, normal, hover):
            btn.SetBackgroundColour(normal)
            btn.Bind(wx.EVT_ENTER_WINDOW, lambda e: btn.SetBackgroundColour(hover))
            btn.Bind(wx.EVT_LEAVE_WINDOW, lambda e: btn.SetBackgroundColour(normal))

        self.shops_data.append({
            "id": id, "name": name, "type": type,
            "email": email, "phone": phone,
            "message": message, "followup": followup,
            "validdate": validdate, "count":count
        })
        # Extract country code using regex and map to country name
        match = re.match(r'(\+\d+)', phone)
        country_code = match.group(1) if match else ''
        country = COUNTRY_MAP.get(country_code, "Unknown")


        card = wx.Panel(self.shop_list_panel, style=wx.BORDER_SIMPLE)
        card.SetBackgroundColour(wx.Colour(255, 255, 255))
        card.SetMinSize((500, 350))
        card.SetWindowStyleFlag(wx.BORDER_THEME)
        card.SetDoubleBuffered(True)

        sizer = wx.BoxSizer(wx.VERTICAL)
        card.SetSizer(sizer)

        # Header Section
        header = wx.BoxSizer(wx.HORIZONTAL)
        title_col = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(card, label=f"{name} / {country}")
        title.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title_col.Add(title)

        subtitle = wx.StaticText(card, label=f"Type: {type}")
        subtitle.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        title_col.Add(subtitle, 0, wx.TOP, 2)

        header.Add(title_col, 1, wx.LEFT | wx.EXPAND, 15)

        # Action Icons
        icon_sizer = wx.BoxSizer(wx.HORIZONTAL)
        for icon_path, handler in [
            ("icons/products-n.png", lambda e, sid=id: self.on_products(e, sid)),
            ("icons/upload-n.png", lambda e, sid=id: self.on_upload(e, sid)),
            ("icons/cookies-n.png", lambda e, sid=id, name=name: self.on_cookies(sid, name)),
            ("icons/edit-n.png", lambda e: self.on_edit(card, name, type)),
            ("icons/delete-n.png", lambda e: self.on_delete(card, id))
        ]:
            full_icon_path = resource_path(icon_path)
            bmp = safe_bitmap(full_icon_path)
            btn = wx.BitmapButton(card, bitmap=bmp, size=(32, 32))
            btn.SetBackgroundColour(wx.Colour(255, 255, 255))
            hover_effect(btn, wx.Colour(255, 255, 255), wx.Colour(230, 230, 230))
            btn.Bind(wx.EVT_BUTTON, handler)
            icon_sizer.Add(btn, 0, wx.LEFT, 8)

        header.Add(icon_sizer, 0, wx.RIGHT, 10)
        sizer.Add(header, 0, wx.TOP | wx.EXPAND, 10)
        sizer.AddSpacer(15)

        # Status Field (e.g., "Stopped" or "Started")
        status_label = wx.StaticText(card, label="Stopped")
        status_label.SetFont(wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        status_label.SetBackgroundColour(wx.Colour(211,211,211))
        status_label.SetForegroundColour(wx.Colour(178, 34, 34)) 
        sizer.Add(status_label, 0, wx.LEFT, 15)

        # # Info Section
        info_section = wx.BoxSizer(wx.HORIZONTAL)

        msg_sizer = wx.BoxSizer(wx.HORIZONTAL)

        msg_label = wx.StaticText(card, label="Messages Sent:")
        msg_label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_EXTRAHEAVY))
        msg_label.SetBackgroundColour(wx.Colour(211, 211, 211))
        msg_sizer.Add(msg_label, 0, wx.RIGHT, 5)

        msg_count = wx.StaticText(card, label=str(count))
        msg_count.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_EXTRAHEAVY))
        msg_sizer.Add(msg_count)

        info_section.Add(msg_sizer, 0, wx.ALIGN_CENTER_VERTICAL)

        line = wx.Panel(card, size=(2, 30))  # 2px wide, 30px tall
        line.SetBackgroundColour(wx.Colour(211, 211, 211))
        info_section.AddSpacer(10)
        info_section.Add(line, 0, wx.ALIGN_CENTER_VERTICAL)
        info_section.AddSpacer(10)

        mod_sizer = wx.BoxSizer(wx.HORIZONTAL)

        mod_label = wx.StaticText(card, label="Last Modified:")
        mod_label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_HEAVY))
        mod_label.SetBackgroundColour(wx.Colour(211, 211, 211))
        mod_sizer.Add(mod_label, 0, wx.RIGHT, 5)

        mod_value = wx.StaticText(card, label=str(last_modified))
        mod_value.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_HEAVY))
        mod_sizer.Add(mod_value)
        info_section.Add(mod_sizer, 0, wx.ALIGN_CENTER_VERTICAL)

        sizer.Add(info_section, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 30)
        sizer.AddSpacer(10)

        log_box = wx.TextCtrl(card, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(-1, 80))
        log_box.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        log_box.SetBackgroundColour(wx.Colour(250, 250, 250))
        log_box.SetForegroundColour(wx.Colour(60, 60, 60))
        log_box.Hide()
        sizer.Add(log_box, 0, wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 15)

        card.log_box = log_box  # 🔁 store reference

        # Start/Stop Button
        bottom = wx.BoxSizer(wx.HORIZONTAL)
        bottom.AddStretchSpacer(1)

        btn = button.GenButton(card, label="Start", size=(90, 35))
        btn.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        btn.SetBackgroundColour(wx.Colour(65, 105, 225))
        btn.SetForegroundColour(wx.WHITE)

        normal_color = wx.Colour(65, 105, 225)  # Start = blue
        hover_color = wx.Colour(100, 149, 237)

        if btn.GetLabel() == "Stop":
            normal_color = wx.Colour(220, 20, 60)  # Stop = red
            hover_color = wx.Colour(255, 69, 0)    # Lighter red-orange

        hover_effect(btn, normal_color, hover_color)

        btn.Bind(wx.EVT_BUTTON, lambda event, b=btn, label=status_label, shop_name=name: self.toggle_start_stop(event, b,label, shop_name, card))
        bottom.Add(btn, 0, wx.RIGHT | wx.BOTTOM, 10)

        sizer.AddStretchSpacer(1)
        sizer.Add(bottom, 0, wx.EXPAND)

        self.shop_list_panel.wrap_sizer.AddSpacer(40)
        self.shop_list_panel.wrap_sizer.Add(card, 0, wx.ALL, 20)
        self.shop_list_panel.wrap_sizer.Layout()
        self.shop_list_panel.FitInside()

    def load_shops_from_db(self):
        print("Loading shops from DB...")
        self.shops_data.clear()
        # Destroy all existing children
        for child in self.shop_list_panel.GetChildren():
            child.Destroy()

        self.shop_list_panel.wrap_sizer.Clear()

        shops = fetch_shops()
        if not shops:
            print("⚠️ No shops found.")
            shops = []
        else:
            print("🛒 Shops loaded from DB:")
            for shop in shops:
                print(f" - {shop['name']}")

        for shop in shops:
            try:
                self.add_shop_card(**shop)
            except Exception as e:
                print(f"Error adding shop card: {e} with data {shop}")

        self.shop_list_panel.wrap_sizer.Layout()
        self.shop_list_panel.FitInside()
    
    def refresh_ui_with_shops(self, updated_shops):
        # Clear current shop data and UI cards
        self.shops_data.clear()
        for child in self.shop_list_panel.GetChildren():
            child.Destroy()

        self.shop_list_panel.wrap_sizer.Clear()

        # Add updated shops back into the UI
        for shop in updated_shops:
            try:
                self.add_shop_card(**shop)
            except Exception as e:
                print(f"[refresh_ui_with_shops] Error adding shop card: {e} with data {shop}")

        self.shop_list_panel.wrap_sizer.Layout()
        self.shop_list_panel.FitInside()

    def reload_shops(self):
        updated_shops = fetch_shops()
        self.refresh_ui_with_shops(updated_shops)
        
class ShopListPanel(wx.ScrolledWindow):
    def __init__(self, parent):
        super().__init__(parent, style=wx.VSCROLL)
        self.SetScrollRate(20, 20)
        self.SetBackgroundColour(wx.Colour(245, 245, 245))

        self.wrap_sizer = wx.WrapSizer(wx.HORIZONTAL)
        self.SetSizer(self.wrap_sizer)
