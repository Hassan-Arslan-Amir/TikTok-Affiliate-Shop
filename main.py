import wx
from login_panel import LoginPanel
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="TikTok Affiliate Shop", size=(1000, 800))
        icon_path = resource_path("icons/tiktok-m.ico") 
        self.SetIcon(wx.Icon(icon_path))
        self.panel = None
        self.switch_panel(LoginPanel)
        self.Centre()
        self.Show()

    def switch_panel(self, panel_class):
        if self.panel:
            self.panel.Destroy()
        self.panel = panel_class(self)
        self.panel.Layout()
        self.Layout()       
        self.panel.Refresh() 

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame()
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
