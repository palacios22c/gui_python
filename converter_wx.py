# converter_wx.py
# -*- coding: utf-8 -*-

'''
Converter of lenght, mass, time and temperature
(wxPython module)

SI units and Imperial units
'''

# Módulo wxPython
try:
    import wx
except ImportError:                                                                     # Error si no se encuentra el módulo
    raise(ImportError,"The wxPython module is required.")

# Base units:
# - Length: meter (m)
# - Mass: kilogram (kg)
# - Time: second (s)
# Temperature uses formulas, not factors.

CONVERSION_FACTORS = {
    "Length": {
        # SI units
        "m": 1,
        "km": 1000,
        "cm": 0.01,
        "mm": 0.001,

        # Imperial units
        "in": 0.0254,
        "ft": 0.3048,
        "yd": 0.9144,
        "mi": 1609.34
    },

    "Mass": {
        # SI units
        "kg": 1,
        "g": 0.001,
        "mg": 0.000001,

        # Imperial units
        "oz": 0.0283495,
        "lb": 0.453592
    },

    "Time": {
        "s": 1,
        "min": 60,
        "h": 3600
    },

    "Area": {
        # SI units
        "m²": 1,
        "km²": 1_000_000, 
        "cm²": 0.0001,
        "mm²": 0.000001,
        "ha": 10_000, 
        "a": 100,

        # Imperial units
        "in²": 0.00064516,
        "ft²": 0.092903,
        "yd²": 0.836127,
        "mi²": 2_589_988.110336,
        "acre": 4046.8564224 },
}

UNITS = {
    "Length": ["m", "km", "cm", "mm", "in", "ft", "yd", "mi"],
    "Mass": ["kg", "g", "mg", "oz", "lb"],
    "Time": ["s", "min", "h"],
    "Temperature": ["C", "F", "K"],
    "Area": ["m²", "km²", "cm²", "mm²", "ha", "a", "in²", "ft²", "yd²", "mi²", "acre"]

}

def convert_temperature(value, from_u, to_u):
    '''Convert temperature between Celsius, Fahrenheit, and Kelvin'''

    # Convert from source unit to Celsius
    if from_u == "C":
        c = value
    elif from_u == "F":
        c = (value - 32) * 5/9
    elif from_u == "K":
        c = value - 273.15

    if to_u == "C":
        return c
    elif to_u == "F":
        return c * 9/5 + 32
    elif to_u == "K":
        return c + 273.15

# Convert non-temperature units
def convert_generic(value, from_unit, to_unit, category):
    '''Convert using base-unit normalization'''
    factors = CONVERSION_FACTORS[category]
    
    # Convert to base unit
    value_in_base = value * factors[from_unit]

    # Convert from base unit to target unit
    result = value_in_base / factors[to_unit]

    return result

# GUI Class
class Converter(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Unit Converter", size=(360, 310))

        # Menu bar
        menubar = wx.MenuBar()

        # File menu
        file_menu = wx.Menu()
        exit_item = file_menu.Append(wx.ID_EXIT, "Salir\tCtrl+Q")
        menubar.Append(file_menu, "Archivo")

        # Theme menu
        theme_menu = wx.Menu()
        dark_item = theme_menu.Append(wx.ID_ANY, "Tema oscuro")
        light_item = theme_menu.Append(wx.ID_ANY, "Tema claro")
        menubar.Append(theme_menu, "Tema")
        self.SetMenuBar(menubar)

        # Bind events
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_MENU, self.on_dark_theme, dark_item)
        self.Bind(wx.EVT_MENU, self.on_light_theme, light_item)

        # Panel + widgets
        panel = wx.Panel(self)

        self.value_input = wx.TextCtrl(panel)
        self.category_combo = wx.ComboBox(panel, choices=list(UNITS.keys()), style=wx.CB_READONLY)
        self.from_combo = wx.ComboBox(panel, style=wx.CB_READONLY)
        self.to_combo = wx.ComboBox(panel, style=wx.CB_READONLY)
        self.result_label = wx.StaticText(panel, label="Result: ")
        self.convert_button = wx.Button(panel, label="Convert")

        # Layout
        main = wx.BoxSizer(wx.VERTICAL)

        def add_row(text, widget):
            row = wx.BoxSizer(wx.HORIZONTAL)
            row.Add(wx.StaticText(panel, label=text), 0, wx.ALL | wx.CENTER, 5)
            row.Add(widget, 1, wx.ALL | wx.EXPAND, 5)
            main.Add(row, 0, wx.EXPAND)

        rows = [
            ("Value:", self.value_input),
            ("Category:", self.category_combo),
            ("From:", self.from_combo),
            ("To:", self.to_combo)
        ]

        for label, widget in rows:
            add_row(label, widget)

        main.Add(self.convert_button, 0, wx.ALL | wx.CENTER, 10)
        main.Add(self.result_label, 0, wx.ALL | wx.CENTER, 10)

        panel.SetSizer(main)

        # Events
        self.category_combo.Bind(wx.EVT_COMBOBOX, self.update_units)
        self.convert_button.Bind(wx.EVT_BUTTON, self.do_conversion)

        # Initialize
        self.category_combo.SetSelection(0)
        self.update_units()

        self.Show()

    def apply_theme(self, bg, panel_bg, text, button_bg, combo_bg, combo_fg):
        '''Apply the selected theme'''
        self.SetBackgroundColour(bg)
        panel = self.GetChildren()[0]
        panel.SetBackgroundColour(panel_bg)

        # Inputs
        self.value_input.SetBackgroundColour("white" if text == "black" else button_bg)
        self.value_input.SetForegroundColour(text)

        for combo in (self.category_combo, self.from_combo, self.to_combo):
            combo.SetBackgroundColour(combo_bg)
            combo.SetForegroundColour(combo_fg)

        # Button
        self.convert_button.SetBackgroundColour(button_bg)
        self.convert_button.SetForegroundColour(text)

        # Labels
        for child in panel.GetChildren():
            if isinstance(child, wx.StaticText):
                child.SetForegroundColour(text)

        self.Refresh()

    def on_light_theme(self, event):
        self.apply_theme(
            "#F0F0F0", "#FFFFFF", "black",
            "#ADD8E6", "#778899", "black"
        )

    def on_dark_theme(self, event):
        self.apply_theme(
            "#1E1E1E", "#2C2C2C", "white",
            "#3A3A3A", "#3A3A3A", "white"
        )

    def update_units(self, event=None):
        '''Update unit dropdowns when category changes'''
        units = UNITS.get(self.category_combo.GetValue(), [])
        self.from_combo.Set(units)
        self.to_combo.Set(units)
        if units:
            self.from_combo.SetSelection(0)
            self.to_combo.SetSelection(0)

    def do_conversion(self, event):
        '''Perform the conversion and update the result label'''
        try:
            value = float(self.value_input.GetValue())
            cat = self.category_combo.GetValue()
            f = self.from_combo.GetValue()
            t = self.to_combo.GetValue()

            result = convert_temperature(value, f, t) if cat == "Temperature" \
                     else convert_generic(value, f, t, cat)

            self.result_label.SetLabel(f"Result: {result:.6g} {t}")

        except ValueError:
            self.result_label.SetLabel("Error: invalid value")

    def on_exit(self, event):
        '''Close the app'''
        self.Close()

# Main app
if __name__ == "__main__":
    app = wx.App()
    Converter()
    app.MainLoop()
