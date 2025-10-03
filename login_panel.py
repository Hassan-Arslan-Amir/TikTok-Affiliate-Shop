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

class LoginPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.background = wx.Bitmap(resource_path("assets/technology.jpg"), wx.BITMAP_TYPE_JPEG)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        self.SetBackgroundColour(wx.Colour(240, 240, 245))
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Container with white background and border
        container = wx.Panel(self, style=wx.BORDER_SIMPLE | wx.TRANSPARENT_WINDOW)
        container.SetBackgroundColour(wx.Colour(0, 0, 0))
        container_sizer = wx.BoxSizer(wx.VERTICAL)
        container_sizer.SetMinSize((450, 240))

        # Title
        title = wx.StaticText(container, label="Welcome Back")
        title_font = wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        title.SetForegroundColour(wx.Colour(255, 255, 255))
        container_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)

        # Username
        user_label = wx.StaticText(container, label="Username:")
        user_label_font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        user_label.SetFont(user_label_font)
        user_label.SetForegroundColour(wx.Colour(255, 255, 255))
        container_sizer.Add(user_label, 0, wx.LEFT | wx.TOP, 10)

        self.username_txt = wx.TextCtrl(container, size=(-1, 40))
        self.username_txt.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.username_txt.SetValue("admin")
        self.username_txt.SetForegroundColour(wx.Colour(50, 50, 90))
        container_sizer.Add(self.username_txt, 0, wx.ALL | wx.EXPAND, 10)

        # Password
        pass_label = wx.StaticText(container, label="Password:")
        pass_label_font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        pass_label.SetFont(pass_label_font)
        pass_label.SetForegroundColour(wx.Colour(255, 255, 255))
        container_sizer.Add(pass_label, 0, wx.LEFT | wx.TOP, 10)

        self.password_txt = wx.TextCtrl(container, style=wx.TE_PASSWORD, size=(-1, 40))
        self.password_txt.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.password_txt.SetValue("password")
        self.password_txt.SetForegroundColour(wx.Colour(50, 50, 90))
        container_sizer.Add(self.password_txt, 0, wx.ALL | wx.EXPAND, 10)

        # Login Button
        self.login_btn = button.GenButton(container, label="Login", size=(100, 50))
        self.login_btn.SetBackgroundColour(wx.Colour(65, 105, 225))  # Steel blue
        self.login_btn.SetForegroundColour(wx.WHITE)
        self.login_btn.SetFont(wx.Font(13, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.login_btn.Bind(wx.EVT_BUTTON, self.on_login)
        self.login_btn.Bind(wx.EVT_ENTER_WINDOW, self.on_button_hover)
        self.login_btn.Bind(wx.EVT_LEAVE_WINDOW, self.on_button_leave)
        container_sizer.Add(self.login_btn, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 15)

        # Message Label
        self.message_lbl = wx.StaticText(container, label="")
        container_sizer.Add(self.message_lbl, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        container.SetSizer(container_sizer)

        # Add the container to the main panel, centered
        main_sizer.AddStretchSpacer(1)
        main_sizer.Add(container, 0, wx.ALIGN_CENTER)
        main_sizer.AddStretchSpacer(1)
        
        self.SetSizer(main_sizer)

    def on_button_hover(self, event):
        self.login_btn.SetBackgroundColour(wx.Colour(70, 130, 180))
        self.login_btn.Refresh()

    def on_button_leave(self, event):
        self.login_btn.SetBackgroundColour(wx.Colour(65, 105, 225))
        self.login_btn.Refresh()

    def on_login(self, event):
        username = self.username_txt.GetValue()
        password = self.password_txt.GetValue()

        # Dummy check for demonstration
        if username == "admin" and password == "password":
            self.message_lbl.SetLabel("Login successful!")
            self.message_lbl.SetForegroundColour(wx.Colour(0, 128, 0))
            # Navigate to home panel
            from home_panel import HomePanel
            self.GetParent().switch_panel(HomePanel)
        else:
            self.message_lbl.SetLabel("Invalid username or password")
            self.message_lbl.SetForegroundColour(wx.Colour(255, 0, 0))

    def on_paint(self, event):
            dc = wx.AutoBufferedPaintDC(self)
            dc.Clear()

            # Stretch the image to panel size
            size = self.GetClientSize()
            img = self.background.ConvertToImage().Scale(size.width, size.height)
            dc.DrawBitmap(wx.Bitmap(img), 0, 0)