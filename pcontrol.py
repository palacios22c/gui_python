# pcontrol.py
# -*- coding: utf-8 -*-

'''
Creación de un panel de control utilizando el módulo por defecto, Tkinter

En este ejemplo se tiene 4 productos, y un número variable de elementos de cada uno de los productos.
Las opciones implementadas son:
- Mostrar la cantidad de elementos que hay para un producto (elegido por el usuario)
- Aumentar (añadir) el número de elementos de uno de los productos.
	(El usuario elige la cantidad y el producto correspondiente)
'''

# Módulos
from tkinter import *
from tkinter import messagebox

def elementos(cantidad, producto):
	'''Método que muestra en una ventana la cantidad disponible para un producto cualquiera'''
	messagebox.showinfo(producto,"Disponemos de %d elementos de %s"%(cantidad,producto))

def masElementos():
	'''Método para mostrar una nueva (new) ventana y añadir elementos a un producto seleccionado

	- Se crea un listado de los productos
	- Se añade una caja para poder introducir un número
	- Finalmente el botón para sumar la cantidad introducida por el usuario a la cantidad que se tiene en memoria
	'''
	new = Toplevel() # Creamos una nueva ventana
	new.geometry("200x100+50+50") # Tamaño y posición de la ventana
	variable = StringVar(new)
	variable.set("Seleccione un producto") # Valor por defecto
	w = OptionMenu(new, variable, "Producto 1", "Producto 2", "Producto 3", "Producto 4")
	w.pack(fill=X) # Ocupada todo el ancho de la ventana

	# Creación de una etiqueta
	var = StringVar()
	var.set("¿Qué cantidad quiere añadir?")
	label = Label(new, textvariable=var, height=1)
	label.pack()

	# Creación de una caja de texto
	cantidad = StringVar()
	caja = Entry(new, textvariable=cantidad)
	caja.pack()

	# Creación de un botón que llama a la función add_elements
	button = Button(new, text="Añadir", command=lambda: add_elements(caja.get(), variable.get(), new, caja), width=10)
	button.pack(side=BOTTOM)

def add_elements (cantidad, producto, window, caja):
	'''Función para añadir una cantidad de elementos a un producto

	El parámetro window indica la ventana de origen (parent)
	'''

	if cantidad == "":	# No hay ninguna cantidad seleccionada
		messagebox.showerror(parent=window, title="Error", message="No hay ninguna cantidad")
		window.destroy()	# Cerramos la ventana windows
	elif producto == "Seleccione un producto": # No hay ningún producto seleccionado
		messagebox.showwarning(parent=window, title="Sin producto", message="No se ha seleccionado ningún producto")
	else:
		if producto == "Producto 1":	# Caso: Producto 1
			global p1
			try:
				p1 += int(cantidad)
			except ValueError:
				messagebox.showwarning(parent=window, title="Valor desconocido", message="La cantidad introducida no es un valor entero")
			else:
				caja.delete(0,'end')
		if producto == "Producto 2":	# Caso: Producto 2
			global p2
			try:
				p2 += int(cantidad)
			except ValueError:
				messagebox.showwarning(parent=window, title="Valor desconocido", message="La cantidad introducida no es un valor entero")
			else:
				caja.delete(0,'end')
		if producto == "Producto 3":	# Caso: Producto 3
			global p3
			try:
				p3 += int(cantidad)
			except ValueError:
				messagebox.showwarning(parent=window, title="Valor desconocido", message="La cantidad introducida no es un valor entero")
			else:
				caja.delete(0,'end')
		if producto == "Producto 4":	# Caso: Producto 2
			global p4
			try:
				p4 += int(cantidad)
			except ValueError:
				messagebox.showwarning(parent=window, title="Valor desconocido", message="La cantidad introducida no es un valor entero")
			else:
				caja.delete(0,'end')

# Ejemplo: Inicializamos los valores de la cantidad de los productos de los que disponemos
p1, p2, p3, p4 = 1, 10, 50, 100

# Creamos (un gestor de) la ventana principal, root
root = Tk()
root.title("Panel de control")		# Título de la ventana

# Boton del producto 1
button1 = Button(root, text="Producto 1", command=lambda: elementos(p1, 'Producto 1'), width=15)
button1.grid(row=0)

# Boton del producto 2
button2 = Button(root, text="Producto 2", command=lambda: elementos(p2, 'Producto 2'), width=15)
button2.grid(row=0, column=2)

# Boton del producto 3
button3 = Button(root, text="Producto 3", command=lambda: elementos(p3, 'Producto 3'), width=15)
button3.grid(row=1)

# Boton del producto 4
button4 = Button(root, text="Producto 4", command=lambda: elementos(p4, 'Producto 4'), width=15)
button4.grid(row=1, column=2)

# Boton para abrir una ventana nueva y añadir una cantidad de elementos
button4 = Button(root, text="Añadir", command=masElementos, width=10)
button4.grid(row=2, column=1)

# Cargamos la ventana
root.mainloop()
