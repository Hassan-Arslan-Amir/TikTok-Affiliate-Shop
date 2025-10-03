import wx
from wx.lib.plot import PlotCanvas, PolyLine, PlotGraphics
import wx.lib.buttons as button
from db_utils import get_all_shops, get_shop_summary, get_combined_summary

class RoundedPanel(wx.Panel):
    def __init__(self, parent, size, bg_color=wx.Colour(255, 255, 255), radius=15):
        super().__init__(parent, size=size)
        self.bg_color = bg_color
        self.radius = radius
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        dc.SetBrush(wx.Brush(self.bg_color))
        dc.SetPen(wx.Pen(self.bg_color))
        width, height = self.GetSize()
        dc.DrawRoundedRectangle(0, 0, width, height, self.radius)

class ReportingPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        nav_panel = wx.Panel(self, size=(-1, 60))
        nav_panel.SetBackgroundColour(wx.Colour(0, 0, 0))  # Black navbar
        nav_sizer = wx.BoxSizer(wx.HORIZONTAL)
        nav_panel.SetSizer(nav_sizer)

        # TikTok Shop title on the left
        title = wx.StaticText(nav_panel, label="TikTok Shop")
        title.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour(wx.WHITE)
        nav_sizer.Add(title, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 20)

        # Stretch spacer between title and buttons
        nav_sizer.AddStretchSpacer(1)

        # Home button
        home_btn = self.create_rounded_button(nav_panel, "Home")
        home_btn.Bind(wx.EVT_BUTTON, self.go_to_home)
        nav_sizer.Add(home_btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)

        # Shop button
        shop_btn = self.create_rounded_button(nav_panel,"Shop")
        shop_btn.Bind(wx.EVT_BUTTON, self.go_to_shop)
        nav_sizer.Add(shop_btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)

        # Add nav bar to main layout
        self.main_sizer.Add(nav_panel, 0, wx.EXPAND | wx.TOP, 0)
  
        # --- Shop Dropdown ---
        try:
            shop_names = get_all_shops()
        except Exception as e:
            wx.MessageBox(f"Error loading shops: {e}", "Database Error", wx.ICON_ERROR)
            shop_names = []

        self.shop_combo = wx.ComboBox(
            self, choices=["Select Shop"] + shop_names,
            style=wx.CB_READONLY, size=(200, 40)
        )
        self.shop_combo.SetValue("Select Shop")
        self.shop_combo.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.shop_combo.SetBackgroundColour(wx.Colour(245, 245, 255))
        self.shop_combo.SetForegroundColour(wx.Colour(40, 40, 60))
        self.shop_combo.Bind(wx.EVT_COMBOBOX, self.on_shop_selected)

        self.main_sizer.Add(self.shop_combo, 0, wx.LEFT | wx.TOP, 20)

        # Placeholder for summary box (will be created dynamically)
        self.summary_wrapper = None

        # --- Message Boxes ---
        container_sizer = wx.BoxSizer(wx.HORIZONTAL)
        container_sizer.AddStretchSpacer(1)

        # We will update message boxes dynamically from summary data
        self.message_data = {}

        self.message_boxes = []  # store created message boxes to update them later

        main_message_titles = ["Daily message sent", "Weekly message sent", "Monthly message sent"]

        for i, title in enumerate(main_message_titles):
            box = self.create_message_box(title, 0)  # start with 0, update later
            container_sizer.Add(box, 0, wx.ALL, 15)
            if i < len(main_message_titles) - 1:
                container_sizer.AddSpacer(50)
            self.message_boxes.append(box)

        container_sizer.AddStretchSpacer(1)
        self.main_sizer.Add(container_sizer, 0, wx.EXPAND | wx.TOP, 100)
        # Load combined summary initially
        print("message_boxes exists:", hasattr(self, 'message_boxes'))
        self.update_summary(self.get_combined_summary())

        self.SetSizer(self.main_sizer)

    def create_rounded_button(self, parent, label):
        btn = button.GenButton(parent, label=label, size=(130, 40))
        btn.SetBackgroundColour(wx.Colour(0,0,0))
        btn.SetForegroundColour(wx.WHITE)
        btn.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        btn.SetWindowStyleFlag(wx.BORDER_NONE)
        return btn

    def create_message_box(self, title, value):
        panel = RoundedPanel(self, size=(450, 300), bg_color=wx.Colour(255, 255, 255))

        box_sizer = wx.BoxSizer(wx.VERTICAL)
        title_row = wx.BoxSizer(wx.HORIZONTAL)

        title_text = wx.StaticText(panel, label=title)
        title_text.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title_text.SetForegroundColour(wx.Colour(0, 0, 0))

        value_text = wx.StaticText(panel, label=f"{value}")
        value_text.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        value_text.SetForegroundColour(wx.Colour(100, 200, 255))

        title_row.Add(title_text, 1, wx.LEFT, 10)
        title_row.Add(value_text, 0, wx.RIGHT, 10)

        box_sizer.Add(title_row, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 10)
        chart = LineChart(panel, [value * 0.3, value * 0.6, value * 0.8, value, value * 0.9])
        box_sizer.Add(chart, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 12)

        panel.SetSizer(box_sizer)

        # Save references to value_text and chart for updates
        panel.value_text = value_text
        panel.chart = chart

        return panel

    def go_to_shop(self, event):
        from shop_panel import ShopPanel
        self.GetParent().switch_panel(ShopPanel)

    def go_to_home(self, event):
        from home_panel import HomePanel
        self.GetParent().switch_panel(HomePanel)

    def on_shop_selected(self, event):
        shop_name = self.shop_combo.GetValue()
        if shop_name == "Select Shop":
            summary = self.get_combined_summary()
        else:
            summary = self.get_shop_summary(shop_name)
        self.update_summary(summary)

    def get_shop_summary(self, shop_name):
        try:
            return get_shop_summary(shop_name)
        except Exception as e:
            wx.MessageBox(f"Failed to load summary for shop {shop_name}: {e}", "Error", wx.ICON_ERROR)
            return {
                "Total messages sent": 0,
                "Daily message sent": 0,
                "Weekly message sent": 0,
                "Monthly message sent": 0
            }

    def get_combined_summary(self):
        try:
            return get_combined_summary()
        except Exception as e:
            wx.MessageBox(f"Failed to load combined summary: {e}", "Error", wx.ICON_ERROR)
            return {
                "Total messages sent": 0,
                "Daily message sent": 0,
                "Weekly message sent": 0,
                "Monthly message sent": 0
            }

    def update_summary(self, summary_data):
        if self.summary_wrapper:
            self.main_sizer.Detach(self.summary_wrapper)
            self.summary_wrapper.Clear(True)

        self.summary_wrapper = wx.BoxSizer(wx.HORIZONTAL)
        top_container = RoundedPanel(self, size=(1500, 150), bg_color=wx.Colour(255, 255, 255))
        top_container_sizer = wx.BoxSizer(wx.HORIZONTAL)

        for title in ["Total messages sent", "Daily message sent", "Weekly message sent", "Monthly message sent"]:
            value = summary_data.get(title, 0)
            panel = wx.Panel(top_container)
            panel.SetBackgroundColour(wx.Colour(255, 255, 255))

            vbox = wx.BoxSizer(wx.VERTICAL)

            label_title = wx.StaticText(panel, label=title)
            label_title.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            label_title.SetForegroundColour(wx.Colour(0, 0, 0))

            label_value = wx.StaticText(panel, label=str(value))
            label_value.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            label_value.SetForegroundColour(wx.Colour(70, 130, 180))

            vbox.Add(label_title, 0, wx.BOTTOM, 5)
            vbox.Add(label_value, 0)

            panel.SetSizer(vbox)
            top_container_sizer.Add(panel, 1, wx.ALL | wx.EXPAND, 20)

        top_container.SetSizer(top_container_sizer)
        self.summary_wrapper.AddStretchSpacer(1)
        self.summary_wrapper.Add(top_container, 4, wx.EXPAND)
        self.summary_wrapper.AddStretchSpacer(1)

        # Insert or add summary_wrapper safely
        if self.main_sizer.GetItemCount() >= 3:
            self.main_sizer.Insert(2, self.summary_wrapper, 0, wx.EXPAND | wx.TOP, 40)
        else:
            self.main_sizer.Add(self.summary_wrapper, 0, wx.EXPAND | wx.TOP, 40)

        self.Layout()

        # Update message boxes below as well
        self.update_message_boxes(summary_data)

    def update_message_boxes(self, summary_data):
        # Update message box values and charts for daily, weekly, monthly messages
        keys = ["Daily message sent", "Weekly message sent", "Monthly message sent"]
        for i, key in enumerate(keys):
            value = summary_data.get(key, 0)
            panel = self.message_boxes[i]
            panel.value_text.SetLabel(str(value))
            # update chart with new values
            panel.chart.update_data([value * 0.3, value * 0.6, value * 0.8, value, value * 0.9])

class LineChart(wx.Panel):
    def __init__(self, parent, data_points, size=(350, 250)):
        super().__init__(parent, size=size)
        self.canvas = PlotCanvas(self)
        self.canvas.SetInitialSize(size)
        self.canvas.enableLegend = False
        self.canvas.enableGrid = False
        self.canvas.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.update_data(data_points)

    def update_data(self, data_points):
        points = [(i, val) for i, val in enumerate(data_points)]
        line = PolyLine(points, colour='blue', width=2)
        graphics = PlotGraphics([line])
        self.canvas.Draw(graphics)
        self.canvas.Refresh()
        self.canvas.Update()
