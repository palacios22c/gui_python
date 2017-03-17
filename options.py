#options.py
#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
A basic panel with information about foods and prices

There are some foods and drinks. They are distributed in 5 categories:
1. Starters (2 products)
2. Entrées (3 products)
3. Main courses (2 products)
4. Desserts (3 products)
5. Drinks (3 products)

This program shows prices for every element (food or drink) that the waiter/user has chosen.

There is a option in menu bar to quit.
'''

# Modules
from PyQt4 import QtGui, QtCore
import random
import sys

# Global values
foods = ('Beer', 'Coke', 'Crispy Chicken Wings',
    'Fish and Chips', 'Fruit', 'Gazpacho', 'Ice cream',
    'Picarones', 'Salmon', 'Spaghetti', 'Spring rolls',
    'Vegetarian risotto', 'Water')
values = random.sample(range(10,100), len(foods))   # Random integers
prices = dict(zip(foods,values))

# Start class
class Start(QtGui.QMainWindow):
    
    def __init__(self):

        super(Start, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        self.mainFrame = Options()                      # Create an Options class
        self.setCentralWidget(self.mainFrame)           # This is our main Frame

        # Close action
        closeAction = QtGui.QAction('Close', self)
        closeAction.triggered.connect(QtGui.qApp.quit)

        # Create a menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(closeAction)                 # Associate Close action to this submenu
        
        self.setGeometry(200, 200, 300, 200)            # Size and position
        self.setWindowTitle('Options')                  # Windows name
        self.show()

# Options class
class Options(QtGui.QWidget):

    def __init__(self):
 
        super(Options, self).__init__()

        # Create a Combo Box
        opts = QtGui.QComboBox(self)
        # Add main categories of food + drinks
        opts.addItem("Starter")
        opts.addItem(u"Entrée") # Use a unicode codification (accent is problematic)
        opts.addItem("Main Course")
        opts.addItem("Dessert")
        opts.addItem("Drinks")

        # Change buttons (name and enabled) every time user changes category
        opts.activated[str].connect(self.changeButtons)

        # Create buttons
        self.firstButton = QtGui.QPushButton('Crispy Chicken Wings', self)
        self.secondButton = QtGui.QPushButton('Gazpacho', self)
        self.thirdButton = QtGui.QPushButton('', self)  # Third button is empty initially
        self.thirdButton.setEnabled(False)              # And it is disabled

        # Connect all buttons to onActivated method
        self.firstButton.clicked.connect(self.onActivated)
        self.secondButton.clicked.connect(self.onActivated)
        self.thirdButton.clicked.connect(self.onActivated)

        # A text box to show information (Name of product and price)
        self.infoOption = QtGui.QTextEdit('')           # Initial value is empty
        self.infoOption.setStyleSheet("background: transparent")
        self.infoOption.setReadOnly(True)               # User cannot change it manually
        self.infoOption.setAlignment(QtCore.Qt.AlignCenter)

        # Create a layout (Grid layout in this example) and put the elements (combobox,
        # buttons and text box)
        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(opts,0,0)
        mainLayout.addWidget(self.firstButton,2,0)
        mainLayout.addWidget(self.secondButton,2,1)
        mainLayout.addWidget(self.thirdButton,2,2)
        mainLayout.addWidget(self.infoOption,3,0,2,0)

        self.setLayout(mainLayout)
        
    def onActivated(self):
        '''Show a message
        
        Product + its price
        '''

        product = self.sender().text()
        price = self.checkPrice(product)
        self.infoOption.setText(product + '\nPrice: ' + str(price))

    def changeButtons(self, text):
        '''Change button's name and enable/disable them'''

        # Text box cleared
        self.infoOption.setText('')

        # Enable all buttons
        self.firstButton.setEnabled(True)
        self.secondButton.setEnabled(True)
        self.thirdButton.setEnabled(True)

        # According to every food category show a text in button and disable it
        if text == 'Starter':
            self.firstButton.setText('Crispy Chicken Wings')
            self.secondButton.setText('Gazpacho')
            self.thirdButton.setText('')
            self.thirdButton.setEnabled(False)
        elif text == u'Entrée':
            self.firstButton.setText('Fish and Chips')
            self.secondButton.setText('Spaghetti')
            self.thirdButton.setText('Spring rolls')
            # self.thirdButton.setEnabled(True)         # It is similar to line before if-conditional
        elif text == 'Main Course':
            self.firstButton.setText('Salmon')
            self.secondButton.setText('Vegetarian risotto')
            self.thirdButton.setText('')
            self.thirdButton.setEnabled(False)
        elif text == 'Dessert':
            self.firstButton.setText('Fruit')
            self.secondButton.setText('Ice cream')
            self.thirdButton.setText('Picarones')
            # self.thirdButton.setEnabled(True)         # It is similar to line before if-conditional
        elif text == 'Drinks':
            self.firstButton.setText('Beer')
            self.secondButton.setText('Coke')
            self.thirdButton.setText('Water')
            # self.thirdButton.setEnabled(True)         # It is similar to line before if-conditional

        # This is a default case (in this example is not possible to reach it)
        else:
            # All buttons are empty
            self.firstButton.setText('')
            self.secondButton.setText('')
            self.thirdButton.setText('')
            # All buttons are disabled
            self.firstButton.setEnabled(False)
            self.secondButton.setEnabled(False)
            self.thirdButton.setEnabled(False)

    def checkPrice(self, text):
        '''Check the global variable prices
        
        Return a numeric value (according to the variable prices). In this example is an integer
        '''
        
        global prices
        return prices[str(text)]

# Main class
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Start()
    sys.exit(app.exec_())

### Main ###

if __name__ == '__main__':
    main()
