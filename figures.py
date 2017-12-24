# figures.py
# -*- coding: utf-8 -*-

'''
A simple canvas test

Figures are shown every time a button is pressed
'''

# Modules
from tkinter import *
from tkinter import messagebox

def square():
	'''Draw a black square'''
	c.create_rectangle(50, 50, 150, 150, fill="black")
	btnMsg()

def circle():
	'''Draw a yellow circle'''
	c.create_oval(50, 50, 150, 150, fill="yellow")
	btnMsg()

def triangle():
	'''Draw a green triangle'''
	c.create_polygon([50, 50, 100, 100, 50, 150], fill="green")
	btnMsg()

def btnMsg():
	'''Show a message every time a button is pressed'''
    print("A button was pressed")

def clearCnv():
	'''Clear the Canvas'''
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

# CANVAS
c = Canvas(root, width=200, height=200)
c.grid(row=2, columnspan=3)

# Main
mainloop()