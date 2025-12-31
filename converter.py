# converter.py
# -*- coding: utf-8 -*-

'''
Converter of lenght, mass, time and temperature

SI units and Imperial units
'''

# Modules
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox,
    QPushButton, QVBoxLayout, QHBoxLayout
)
import sys

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
    }
}

UNITS = {
    "Length": ["m", "km", "cm", "mm", "in", "ft", "yd", "mi"],
    "Mass": ["kg", "g", "mg", "oz", "lb"],
    "Time": ["s", "min", "h"],
    "Temperature": ["C", "F", "K"]
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
    # Convert from Celsius to target unit
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
class Converter(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Unit Converter")

        # Widgets
        self.value_input = QLineEdit()
        self.category_combo = QComboBox()
        self.from_combo = QComboBox()
        self.to_combo = QComboBox()
        self.result_label = QLabel("Result: ")

        self.convert_button = QPushButton("Convert")

        # CSS for category ComboBox
        self.category_combo.setStyleSheet("""
            QComboBox {
                background-color: #778899;
                color: black;
                padding: 4px;
                border-radius: 4px;
            }
            QComboBox QAbstractItemView {
                background-color: #BBBBBB;
                color: black;
            }
        """)

        # CSS for Convert button
        self.convert_button.setStyleSheet("""
            QPushButton {
                background-color: #ADD8E6;
                color: black;
                padding: 6px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #9CC7D6;
            }
        """)

        self.category_combo.addItems(UNITS.keys())

        # Layouts
        layout = QVBoxLayout()

        # Value row
        row_value = QHBoxLayout()
        row_value.addWidget(QLabel("Value:"))
        row_value.addWidget(self.value_input)
        layout.addLayout(row_value)

        # Category row
        row_cat = QHBoxLayout()
        row_cat.addWidget(QLabel("Category:"))
        row_cat.addWidget(self.category_combo)
        layout.addLayout(row_cat)

        # From row
        row_from = QHBoxLayout()
        row_from.addWidget(QLabel("From:"))
        row_from.addWidget(self.from_combo)
        layout.addLayout(row_from)

        # To row
        row_to = QHBoxLayout()
        row_to.addWidget(QLabel("To:"))
        row_to.addWidget(self.to_combo)
        layout.addLayout(row_to)

        # Convert button
        layout.addWidget(self.convert_button)

        # Result label
        layout.addWidget(self.result_label)

        self.setLayout(layout)

        # Events
        self.category_combo.currentTextChanged.connect(self.update_units)
        self.convert_button.clicked.connect(self.do_conversion)

        # Initialize units
        self.update_units()

    def update_units(self):
        '''Update unit dropdowns when category changes'''
        category = self.category_combo.currentText()
        units = UNITS.get(category, [])

        self.from_combo.clear()
        self.to_combo.clear()

        self.from_combo.addItems(units)
        self.to_combo.addItems(units)

    def do_conversion(self):
        '''Perform the conversion and update the result label'''
        try:
            value = float(self.value_input.text())
            category = self.category_combo.currentText()
            from_unit = self.from_combo.currentText()
            to_unit = self.to_combo.currentText()

            if category == "Temperature": # Convert temperature units
                result = convert_temperature(value, from_unit, to_unit)
            else:						  # Convert non-temperature units
                result = convert_generic(value, from_unit, to_unit, category)

            self.result_label.setText(f"Result: {result:.6g} {to_unit}")

        except ValueError:
            self.result_label.setText("Error: invalid value")

# Main app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Converter()
    window.show()
    sys.exit(app.exec())
