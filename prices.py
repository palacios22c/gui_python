#prices.py
#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
A panel to calculate the total price of several products

There are three items: bikes, cars and trucks

This program has buttons to show prices for every item.
A button to calculate the total price and another button to quit.
'''

# Modules
from fltk import *
import sys

# Global variable (items and prices)
prices = {"bikes": 100.5, "cars": 1250, "trucks": 5750}

# Main window class
class CalculatePrices:

    def __init__(self):
        # Main windows
        self.window = Fl_Double_Window(300, 200)                # Size
        self.window.label("Prices Window")                      # Label for this window

        # Two boxes
        self.box = Fl_Box(10,5,285,20,"Prices")                 # Position, size and text
        self.box.labelfont(FL_BOLD)                             # Font of the text
        self.box1 = Fl_Box(10,30,285,110)                       # Position and size
        self.box1.box(FL_PLASTIC_DOWN_BOX)                      # Box type
        
        ## Five input areas and buttons
        # First Button/ First item
        self.input1 = Fl_Input(110, 35, 100, 25, "Bikes?")      # Text area position, size and label
        self.button1 = Fl_Button(215, 35, 75, 25, "Price")      # Button position, size and label
        self.button1.callback(self.p_items,self.input1)         # Function associated to event

        # Second item
        self.input2 = Fl_Input(110, 70, 100, 25, "Cars?")       # Text area position, size and label
        self.button2 = Fl_Button(215, 70, 75, 25, "Price")      # Button position, size and label
        self.button2.callback(self.p_items,self.input2)         # Function associated to event

        # Third item
        self.input3 = Fl_Input(110, 105, 100, 25, "Trucks?")    # Text area position, size and label
        self.button3 = Fl_Button(215, 105, 75, 25, "Price")     # Button position, size and label
        self.button3.callback(self.p_items,self.input3)         # Function associated to event

        # Last two buttons
        self.button4 = Fl_Button(10, 170, 70, 25, "Total")      # Button position, size and label
        self.button4.callback(self.p_total)                     # Function associated to event
        self.button5 = Fl_Button(220, 170, 70, 25, "Quit")      # Button position, size and label
        self.button5.callback(self.quit)                       # Function associated to event

        # Show the window
        self.window.end()
        self.window.show()
        Fl.run()

    def p_items(self, ptr, item):
        '''Show an alert window with item (bike, car or bike) price'''

        txt = item.label()[:-1].lower()
        fl_alert("Price for every" + txt + "is: " + str(prices[txt]) + " dollars")

    def p_total(self, ptr):
        '''Calculate total price and show an alert window with total'''

        # Get values
        val1 = self.input1.value()
        val2 = self.input2.value()
        val3 = self.input3.value()

        # str -> int
        try:
            val1 = int(val1)
        except ValueError:
            val1 = 0
        try:
            val2 = int(val2)
        except ValueError:
            val2 = 0
        try:
            val3 = int(val3)
        except ValueError:
            val3 = 0

        # Calculate
        total = val1*prices["bikes"] + val2*prices["cars"] + val3*prices["trucks"]

        # Show an alert window
        fl_alert("Total price: " + str(total) + " dollars")

        # Set values to "" (empty)
        self.input1.value("")
        self.input2.value("")
        self.input3.value("")

    def quit(self, ptr):
        '''Exit'''
        return sys.exit(0)

### Main ###

if __name__ == '__main__':
    app = CalculatePrices()
