import wx
import re
import wx.lib.buttons as btn
import wx.adv

class AddShopDialog(wx.Dialog):
    def __init__(self, parent, shop_data=None):
        super().__init__(parent, title="Add Shop", size=(1000, 650))
        self.followup_shown = False  
        self.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.Centre()

        font_label = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        font_input = wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        outer_sizer = wx.BoxSizer(wx.VERTICAL)

        container = wx.Panel(self)
        container.SetBackgroundColour(wx.Colour(211, 211, 211))
        container.SetMinSize((760, 380))

        horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        container.SetSizer(horizontal_sizer)

        # Left Panel
        left_panel = wx.Panel(container)
        left_panel.SetBackgroundColour(wx.Colour(211, 211, 211))
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_panel.SetSizer(left_sizer)

        self.inputs = {}
        fields = ["Name", "Email", "Phone Number"]

        for field in fields:
            label = wx.StaticText(left_panel, label=field)
            label.SetFont(font_label)
            label.SetForegroundColour(wx.Colour(40, 40, 60))
            left_sizer.Add(label, 0, wx.LEFT | wx.RIGHT | wx.TOP, 20)
            if field == "Phone Number":
                phone_sizer = wx.BoxSizer(wx.HORIZONTAL)

                self.country_code = wx.ComboBox(
                    left_panel,
                    choices=["+1 (USA)", "+44 (UK)", "+49 (Germany)"],
                    style=wx.CB_READONLY,
                    size=(100, 35)
                )
                self.country_code.SetFont(font_input)
                self.country_code.SetBackgroundColour(wx.Colour(255, 255, 255))
                self.country_code.SetForegroundColour(wx.Colour(40, 40, 60))
                self.country_code.SetValue("+1 (USA)")

                phone_input = wx.TextCtrl(left_panel, size=(-1, 35))
                phone_input.SetFont(font_input)
                phone_input.SetBackgroundColour(wx.Colour(245, 245, 255))
                phone_input.SetForegroundColour(wx.Colour(40, 40, 60))

                phone_sizer.Add(self.country_code, 0, wx.RIGHT, 10)
                phone_sizer.Add(phone_input, 1, wx.EXPAND)

                left_sizer.Add(phone_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
                self.inputs[field] = phone_input
            else:
                text = wx.TextCtrl(left_panel, size=(-1, 35), style=wx.TE_LEFT)
                text.SetFont(font_input)
                text.SetBackgroundColour(wx.Colour(245, 245, 255))
                text.SetForegroundColour(wx.Colour(40, 40, 60))

                left_sizer.Add(text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
                self.inputs[field] = text

        # Add Static Line separator
        left_sizer.Add(wx.StaticLine(left_panel), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 15)

        # Valid Until Label and Picker (moved here)
        valid_until_label = wx.StaticText(left_panel, label="Valid Until")
        valid_until_label.SetFont(font_label)
        valid_until_label.SetForegroundColour(wx.Colour(40, 40, 60))
        left_sizer.Add(valid_until_label, 0, wx.LEFT | wx.RIGHT | wx.TOP, 20)

        self.valid_until_picker = wx.adv.DatePickerCtrl(
            left_panel,
            style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY
        )
        self.valid_until_picker.SetFont(font_input)
        self.valid_until_picker.SetBackgroundColour(wx.Colour(245, 245, 255))
        self.valid_until_picker.SetForegroundColour(wx.Colour(40, 40, 60))

        today = wx.DateTime.Now()
        self.valid_until_picker.SetRange(today, wx.DefaultDateTime)

        left_sizer.Add(self.valid_until_picker, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 20)
        self.inputs["Valid Until"] = self.valid_until_picker

        # Another Static Line separator
        left_sizer.Add(wx.StaticLine(left_panel), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 15)

        # Shop Type ComboBox
        shop_type_label = wx.StaticText(left_panel, label="Shop Type")
        shop_type_label.SetFont(font_label)
        shop_type_label.SetForegroundColour(wx.Colour(40, 40, 60))
        left_sizer.Add(shop_type_label, 0, wx.LEFT | wx.RIGHT | wx.TOP, 20)

        self.shop_type_choice = wx.ComboBox(
            left_panel, choices=["Target Write", "Open Colab"], style=wx.CB_READONLY, size=(-1, 35)
        )
        self.shop_type_choice.SetFont(font_input)
        self.shop_type_choice.SetBackgroundColour(wx.Colour(245, 245, 255))
        self.shop_type_choice.SetForegroundColour(wx.Colour(40, 40, 60))
        left_sizer.Add(self.shop_type_choice, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        horizontal_sizer.Add(left_panel, 1, wx.EXPAND | wx.ALL, 10)

        # Add vertical line separator
        vline = wx.StaticLine(container, style=wx.LI_VERTICAL)
        horizontal_sizer.Add(vline, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)

        # Right Panel
        right_panel = wx.Panel(container)
        right_panel.SetBackgroundColour(wx.Colour(211, 211, 211))
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_panel.SetSizer(right_sizer)

        message_label = wx.StaticText(right_panel, label="Message")
        message_label.SetFont(font_label)
        message_label.SetForegroundColour(wx.Colour(40, 40, 60))
        right_sizer.Add(message_label, 0, wx.LEFT | wx.RIGHT | wx.TOP, 20)

        message_text = wx.TextCtrl(right_panel, size=(-1, 120), style=wx.TE_MULTILINE)
        message_text.SetFont(font_input)
        message_text.SetBackgroundColour(wx.Colour(245, 245, 255))
        message_text.SetForegroundColour(wx.Colour(40, 40, 60))
        right_sizer.Add(message_text, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        self.inputs["Message"] = message_text

        # Toggle Button for Follow-up
        self.followup_toggle = wx.ToggleButton(right_panel, label="Enable Follow-up")
        self.followup_toggle.SetFont(font_label)
        self.followup_toggle.SetBackgroundColour(wx.Colour(65, 105, 225)) 
        self.followup_toggle.SetForegroundColour(wx.WHITE)
        right_sizer.Add(self.followup_toggle, 0, wx.ALL | wx.TOP, 20)

        # Follow-up Message TextCtrl (initially hidden)
        self.followup_label = wx.StaticText(right_panel, label="Follow-up Message")
        self.followup_label.SetFont(font_label)
        self.followup_label.SetForegroundColour(wx.Colour(40, 40, 60))

        self.followup_text = wx.TextCtrl(right_panel, size=(-1, 120), style=wx.TE_MULTILINE)
        self.followup_text.SetFont(font_input)
        self.followup_text.SetBackgroundColour(wx.Colour(245, 245, 255))
        self.followup_text.SetForegroundColour(wx.Colour(40, 40, 60))

        self.followup_label.Hide()
        self.followup_text.Hide()

        right_sizer.Add(self.followup_label, 0, wx.LEFT | wx.RIGHT | wx.TOP, 20)
        right_sizer.Add(self.followup_text, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        self.inputs["Follow-up Message"] = self.followup_text

        self.followup_toggle.Bind(wx.EVT_TOGGLEBUTTON, self.on_toggle_followup)

        horizontal_sizer.Add(right_panel, 1, wx.EXPAND | wx.ALL, 10)

        # Prefill fields if shop_data provided
        if shop_data:
            self.inputs["Name"].SetValue(shop_data.get("name", ""))
            self.inputs["Email"].SetValue(shop_data.get("email", ""))
            self.inputs["Message"].SetValue(shop_data.get("message", ""))
            followup_msg = shop_data.get("followup", "")
            self.inputs["Follow-up Message"].SetValue(followup_msg or "")
            if followup_msg:
                self.followup_toggle.SetValue(True)
                self.followup_label.Show()
                self.followup_text.Show()
                self.followup_shown = True
            else:
                self.followup_label.Hide()
                self.followup_text.Hide()
                self.followup_shown = False
            self.shop_type_choice.SetValue(shop_data.get("type", ""))

            phone_full = shop_data.get("phone", "")
            if phone_full.startswith("+") and " " in phone_full:
                code, number = phone_full.split(" ", 1)
                #code_mapping = {"+1": "+1 (USA)", "+44": "+44 (UK)", "+49": "+49 (Germany)"}
                code_mapping = {"+1": "+1 (USA)", "+44": "+44 (UK)"}
                self.country_code.SetValue(code_mapping.get(code, "+1 (USA)"))
                self.inputs["Phone Number"].SetValue(number)
            else:
                self.inputs["Phone Number"].SetValue(phone_full)

            valid_until_str = shop_data.get("validdate", "")
            if valid_until_str:
                try:
                    month, day, year = map(int, valid_until_str.split("/"))
                    dt = wx.DateTime.FromDMY(day, month - 1, year)
                    self.valid_until_picker.SetValue(dt)
                except Exception as e:
                    print("Failed to parse validdate:", e)

        # Buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        submit_btn = btn.GenButton(self, label="Submit", size=(120, 45))
        submit_btn.SetBackgroundColour(wx.Colour(65, 105, 225))
        submit_btn.SetForegroundColour(wx.WHITE)
        submit_btn.SetFont(wx.Font(13, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        submit_btn.Bind(wx.EVT_BUTTON, self.on_submit)

        close_btn = btn.GenButton(self, wx.ID_CANCEL, label="Close", size=(120, 45))
        close_btn.SetBackgroundColour(wx.Colour(220, 20, 60))
        close_btn.SetForegroundColour(wx.WHITE)
        close_btn.SetFont(wx.Font(13, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        btn_sizer.Add(submit_btn, 0, wx.RIGHT, 20)
        btn_sizer.Add(close_btn, 0)

        outer_sizer.Add(container, 1, wx.EXPAND | wx.ALL, 20)
        outer_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)

        self.SetSizer(outer_sizer)

    def on_submit(self, event):
        # Fetch values and strip whitespace
        values = {}
        for field in self.inputs:
                if field == "Follow-up Message" and not self.followup_shown:
                    continue
                if field == "Valid Until":
                    values[field] = self.inputs[field].GetValue()
                else:
                    values[field] = self.inputs[field].GetValue().strip()
        shop_type = self.shop_type_choice.GetValue().strip()

        # Check all text fields are filled
        for field, val in values.items():
            if not val:
                wx.MessageBox(f"Please enter the {field}.", "Error", wx.OK | wx.ICON_ERROR)
                return

        # Email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", values["Email"]):
            wx.MessageBox("Invalid Email format. Should be like abc@abc.com", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Phone validation
        phone_digits = values["Phone Number"].replace(" ", "")
        if not phone_digits.isdigit():
            wx.MessageBox("Invalid Phone Number. It must contain only digits.", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        # Validate "Valid Until" date
        valid_until_date = values["Valid Until"]
        if valid_until_date < wx.DateTime.Today():
            wx.MessageBox("Please select a future date for 'Valid Until'.", "Error", wx.OK | wx.ICON_ERROR)
            return
        values["Valid Until"] = valid_until_date.Format("%m/%d/%Y")

        # Check shop type selected
        if not shop_type:
            wx.MessageBox("Please select a Shop Type.", "Error", wx.OK | wx.ICON_ERROR)
            return

        phone_code = self.country_code.GetValue().split()[0]
        values["Phone Number"] = f"{phone_code} {values['Phone Number']}"

        # If validation passes
        wx.MessageBox(f"Shop '{values['Name']}' of type '{shop_type}' added successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
        self.EndModal(wx.ID_OK)

    def get_values(self):
        values = {}
        for field in self.inputs:
            if field == "Valid Until":
                date_obj = self.inputs[field].GetValue()
                values[field] = date_obj.Format("%m/%d/%Y")
            elif field == "Message":
                # Use Follow-up Message if toggle is on
                if self.followup_shown:
                    values[field] = self.inputs["Follow-up Message"].GetValue().strip()
                else:
                    values[field] = self.inputs["Message"].GetValue().strip()
            elif field == "Follow-up Message":
                values[field] = self.inputs["Follow-up Message"].GetValue().strip()
            else:
                values[field] = self.inputs[field].GetValue().strip()
        print("Collected inputs before formatting:", values)  # Debug log
        phone_code = self.country_code.GetValue().split()[0]
        values["Phone Number"] = f"{phone_code} {values['Phone Number']}"
        values["ShopType"] = self.shop_type_choice.GetValue().strip()
        valid_until_date = self.inputs["Valid Until"].GetValue()
        values["Valid Until"] = valid_until_date.Format("%m/%d/%Y")
        print("Final collected values:", values)  # Debug log
        return values

    def on_toggle_followup(self, event):
        self.followup_shown = self.followup_toggle.GetValue()
        if self.followup_shown:
            self.followup_label.Show()
            self.followup_text.Show()
        else:
            self.followup_label.Hide()
            self.followup_text.Hide()
            self.inputs["Follow-up Message"].SetValue("")
        self.Layout()
