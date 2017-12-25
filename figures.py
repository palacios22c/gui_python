# figures.py
# -*- coding: utf-8 -*-

'''
A simple canvas test

Figures are shown every time a button is pressed
'''

# Modules
from tkinter import *
from tkinter import messagebox

defaultSize = 75 # Default size for canvas and figures

def square():
	'''Draw a square'''
	colourDefault = colours.get() # Colour of the selection
	c.create_rectangle(defaultSize, defaultSize, 3*defaultSize, 3*defaultSize, fill=colourDefault)
	btnMsg()

def circle():
	'''Draw a circle'''
	colourDefault = colours.get() # Colour of the selection
	c.create_oval(defaultSize, defaultSize, 3*defaultSize, 3*defaultSize, fill=colourDefault)
	btnMsg()

def triangle():
	'''Draw a triangle'''
	colourDefault = colours.get() # Colour of the selection
	c.create_polygon([defaultSize, defaultSize, 2*defaultSize, 2*defaultSize, defaultSize, 3*defaultSize], fill=colourDefault)
	btnMsg()

def btnMsg():
	'''Show a message every time a button is pressed'''
	print("A button was pressed")

def clearCnv():
	'''Clear the Canvas and set initial values'''
	colours.set("black") # Initial colour
	c.delete("all")
	print( "New Canvas")

def aboutMsg():
	'''Info message'''
	messagebox.showinfo("About...", "Figures example")

root = Tk()
root.title("Figures") # Title

# MENU
menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=clearCnv)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)

helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=aboutMsg)

btnSqr = Button(root, text="Square", command=square).grid(row=0, column=0)
btnCir = Button(root, text="Circle", command=circle).grid(row=0, column=1)
btnTrg = Button(root, text="Triangle", command=triangle).grid(row=0, column=2)

# Choose colour
colours = StringVar()
colours.set("black") # Initial colour

Radiobutton(root, text="Black", variable=colours, value="black").grid(row=1)
Radiobutton(root, text="Yellow", variable=colours, value="yellow").grid(row=1, column=1)
Radiobutton(root, text="Green", variable=colours, value="green").grid(row=1, column=2)

# CANVAS
c = Canvas(root, width=4*defaultSize, height=4*defaultSize)
c.grid(row=2, columnspan=3)

# Main
mainloop()