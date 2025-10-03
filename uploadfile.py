import wx
import csv

class UploadDialog(wx.Dialog):
    def __init__(self, parent, shop_id):
        super().__init__(parent, title="📤 Upload File", size=(420, 220),
                         style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP)
        
        self.shop_id=shop_id
        self.SetBackgroundColour(wx.WHITE)
        self.SetWindowStyle(self.GetWindowStyle() & ~wx.RESIZE_BORDER)
        self.selected_file = None
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.msg = wx.StaticText(self, label="📁 Select the required file.", style=wx.ALIGN_CENTER)
        self.msg.Wrap(350)
        font = self.msg.GetFont()
        font.PointSize += 1
        font.MakeBold()
        self.msg.SetFont(font)
        vbox.Add(self.msg, 0, wx.TOP | wx.BOTTOM | wx.CENTER, 20)

        # Button Row
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.browse_btn = wx.Button(self, label="🔍 Browse", size=(100, 35))
        self.browse_btn.Bind(wx.EVT_BUTTON, self.on_browse)
        self.browse_btn.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.browse_btn.SetForegroundColour(wx.Colour(0, 0, 0))
        self.browse_btn.SetWindowStyleFlag(wx.BORDER_SIMPLE)
        hbox.Add(self.browse_btn, 0, wx.ALL, 10)

        self.ok_btn = wx.Button(self, label="✅ OK", size=(100, 35))
        self.ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)
        self.ok_btn.Disable()
        self.ok_btn.SetBackgroundColour(wx.Colour(180, 230, 200))
        self.ok_btn.SetForegroundColour(wx.Colour(0, 80, 0))
        self.ok_btn.SetWindowStyleFlag(wx.BORDER_SIMPLE)
        hbox.Add(self.ok_btn, 0, wx.ALL, 10)

        vbox.Add(hbox, 0, wx.CENTER)

        self.SetSizer(vbox)

    def on_browse(self, event):
        with wx.FileDialog(self, "Open CSV file", wildcard="CSV files (*.csv)|*.csv",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            path = fileDialog.GetPath()
            if not path.lower().endswith('.csv'):
                wx.MessageBox("⚠️ Please select a .csv file.", "Invalid File", wx.OK | wx.ICON_WARNING)
                return

            self.selected_file = path
            print("File selected in dialog:", self.selected_file)
            self.msg.SetLabel(f"📄 Selected file:\n{self.selected_file}")
            self.msg.Wrap(350)
            self.Layout()
            self.ok_btn.Enable()

    def on_ok(self, event):
        if not self.selected_file:
            wx.MessageBox("⚠️ No file selected!", "Error", wx.OK | wx.ICON_ERROR)
            return
        try:
            names = []
            with open(self.selected_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                # Accept both 'names' and 'Names' columns
                col_name = None
                if 'names' in reader.fieldnames:
                    col_name = 'names'
                elif 'Names' in reader.fieldnames:
                    col_name = 'Names'
                elif 'Name' in reader.fieldnames:
                    col_name = 'Name'
                else:
                    wx.CallAfter(wx.MessageBox, "⚠️ 'names' or 'Names' column not found in the CSV.", "Invalid CSV", wx.OK | wx.ICON_ERROR)
                    return
                for row in reader:
                    if row[col_name].strip():
                        names.append(row[col_name].strip())

            if names:
                wx.CallAfter(lambda: self.process_and_insert_users(names))
        except Exception as e:
            wx.CallAfter(wx.MessageBox,  f"❌ Error reading file:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def process_and_insert_users(self, names):
        dialog = wx.Dialog(self, title="⏳ Fetching Creators from File...", size=(400, 160), style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP)
        panel = wx.Panel(dialog)
        dialog.SetBackgroundColour(wx.WHITE)
        panel.SetBackgroundColour(wx.WHITE)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(panel, label=f"🚀 Fetching Creators from File...")
        label.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        vbox.Add(label, 0, wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 15)

        gauge = wx.Gauge(panel, range=len(names), style=wx.GA_HORIZONTAL)
        vbox.Add(gauge, 0, wx.EXPAND | wx.ALL, 10)
        panel.SetSizer(vbox)
        dialog.Centre()
        dialog.Show()

        def insert(index=0):
            if not dialog or not dialog.IsShownOnScreen():
                return 
            
            if index < len(names):
                from db_utils import get_connection
                conn = get_connection()
                cur = conn.cursor()

                name = names[index]
                cur.execute("SELECT 1 FROM users WHERE shop_id = ? AND name = ?", (self.shop_id, name))
                if not cur.fetchone():
                    cur.execute("INSERT INTO users (shop_id, name, processed) VALUES (?, ?, 0)", (self.shop_id, name))
                    print(f"✅ Added user '{name}' for shop_id '{self.shop_id}'")
                else:
                    print(f"⚠️ Skipped duplicate user '{name}' for shop_id '{self.shop_id}'")
                conn.commit()
                conn.close()

                if gauge:
                    gauge.SetValue(index + 1)
                label.SetLabel(f"🚀 Fetching Creators from File... {index + 1}")
                wx.CallLater(1, lambda: insert(index + 1)) 
            else:
                from db_utils import update_last_modified
                update_last_modified(self.shop_id)

                if dialog and dialog.IsShownOnScreen():
                    dialog.Destroy()

                if self.IsModal():
                    wx.CallAfter(self.EndModal, wx.ID_OK)    
                wx.CallAfter(lambda: self.show_names_popup(names))
        insert()

    def show_names_popup(self, names):
        names = names[:500]

        dialog = wx.Dialog(None, title="⏳ Uploading...", size=(600, 600),
                        style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP)
        dialog.SetBackgroundColour(wx.Colour(250, 250, 250))
        panel = wx.Panel(dialog)
        panel.SetBackgroundColour(wx.WHITE)
        vbox = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(panel, label=f"📤 Uploading Creators to Database...")
        font = label.GetFont()
        font.PointSize += 2
        font.MakeBold()
        label.SetFont(font)
        label.SetForegroundColour(wx.Colour(30, 30, 80))
        vbox.Add(label, 0, wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER, 15)

        progress_bar = wx.Gauge(panel, range=len(names), style=wx.GA_HORIZONTAL)
        vbox.Add(progress_bar, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        scrolled = wx.ScrolledWindow(panel, size=(500, 400), style=wx.VSCROLL | wx.BORDER_SIMPLE)
        scrolled.SetScrollRate(0, 20)
        scrolled.SetBackgroundColour(wx.Colour(240, 240, 240))
        scrolled_sizer = wx.BoxSizer(wx.VERTICAL)
        scrolled.SetSizer(scrolled_sizer)
        vbox.Add(scrolled, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(vbox)
        dialog.Centre()

        def populate_names(index=0):
            if not scrolled or not scrolled.Parent or not scrolled.Parent.IsShown():
                return

            if index < len(names):
                label.SetLabel(f"📤 Uploading Creators to Database...")
                scrolled_sizer.Add(wx.StaticText(scrolled, label=f"{index + 1}. {names[index]}"), 0, wx.LEFT | wx.TOP, 5)
                scrolled.Layout()
                scrolled.FitInside()
                progress_bar.SetValue(index + 1)
                wx.CallLater(1, lambda: populate_names(index + 1))
            else:
                wx.CallLater(2000, dialog.Destroy)  # Auto close after fill
                wx.MessageBox(f"Creators have been added successfully.", "Upload Complete", wx.OK | wx.ICON_INFORMATION)

        wx.CallLater(100, populate_names)
        dialog.Show()
