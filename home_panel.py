import wx
import wx.lib.buttons as button
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class HomePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.background = wx.Bitmap(resource_path("assets/technology.jpg"), wx.BITMAP_TYPE_JPEG)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Top bar with Log Out button
        top_bar = wx.BoxSizer(wx.HORIZONTAL)
        top_bar.AddStretchSpacer(1)

        logout_btn = button.GenButton(self, label="Log Out", size=(100, 50))
        logout_btn.SetBackgroundColour(wx.Colour(65, 105, 225))
        logout_btn.SetForegroundColour(wx.WHITE)
        logout_btn.SetFont(wx.Font(13, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        logout_btn.Bind(wx.EVT_BUTTON, self.go_to_login)
        top_bar.Add(logout_btn, 0, wx.ALL, 15)

        main_sizer.Add(top_bar, 0, wx.EXPAND)
        main_sizer.AddStretchSpacer(1)

        # Horizontal sizer for clickable containers
        container_sizer = wx.BoxSizer(wx.HORIZONTAL)

        reports_panel = self.create_nav_panel("Reports", self.go_to_reporting)
        shops_panel = self.create_nav_panel("Shops", self.go_to_shops)

        container_sizer.AddStretchSpacer(1)
        container_sizer.Add(reports_panel, 0, wx.LEFT | wx.RIGHT, 50)
        container_sizer.Add(shops_panel, 0, wx.LEFT | wx.RIGHT, 50)
        container_sizer.AddStretchSpacer(1)

        main_sizer.Add(container_sizer, 0, wx.EXPAND)
        main_sizer.AddStretchSpacer(1)

        self.SetSizer(main_sizer)

    def create_nav_panel(self, label, handler):
        panel = wx.Panel(self, size=(250, 150))
        normal_color = wx.Colour(100, 160, 210)
        hover_color = wx.Colour(130, 190, 240)

        panel.SetBackgroundColour(normal_color)
        panel.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        text = wx.StaticText(panel, label=label)
        text.SetForegroundColour(wx.WHITE)
        text.SetFont(wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer(1)
        sizer.Add(text, 0, wx.ALIGN_CENTER)
        sizer.AddStretchSpacer(1)
        panel.SetSizer(sizer)

        panel.Bind(wx.EVT_LEFT_DOWN, handler)

        def on_enter(event):
            panel.SetBackgroundColour(hover_color)
            panel.Refresh()
            event.Skip()

        def on_leave(event):
            panel.SetBackgroundColour(normal_color)
            panel.Refresh()
            event.Skip()

        panel.Bind(wx.EVT_ENTER_WINDOW, on_enter)
        panel.Bind(wx.EVT_LEAVE_WINDOW, on_leave)

        return panel

    def go_to_login(self, event):
        from login_panel import LoginPanel
        self.GetParent().switch_panel(LoginPanel)

    def go_to_reporting(self, event):
        from reporting_panel import ReportingPanel
        self.GetParent().switch_panel(ReportingPanel)

    def go_to_shops(self, event):
        print("[DEBUG] Navigating to ShopPanel")
        from shop_panel import ShopPanel
        try:
            self.GetParent().switch_panel(ShopPanel)
            print("[DEBUG] ShopPanel successfully switched")
        except Exception as e:
            print(f"[ERROR] Failed to load ShopPanel: {e}")

    def on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        size = self.GetClientSize()
        img = self.background.ConvertToImage().Scale(size.width, size.height)
        dc.DrawBitmap(wx.Bitmap(img), 0, 0)
