# pcontrol_ttk.py
# -*- coding: utf-8 -*-

'''
Panel de control con ttk (Tkinter moderno)

Opciones implementadas:
- Mostrar cantidad de productos
- Añadir elementos a un producto
'''

# Módulos
import tkinter as tk
from tkinter import ttk, messagebox

class ControlPanel(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Panel de control")
        self.resizable(False, False)
        self.configure(padx=12, pady=12)

        # Ejemplo: Inicializamos los valores de la cantidad de los productos de los que disponemos
        self.products = {
            "Producto 1": 1,
            "Producto 2": 10,
            "Producto 3": 50,
            "Producto 4": 100,
        }

        self._crear_widgets()

    def _crear_widgets(self):
        frame = ttk.Frame(self)
        frame.grid()

        for i, product in enumerate(self.products):
            btn = ttk.Button(
                frame,
                text=product,
                command=lambda p=product: self.mostrar_cantidad(p),
                width=18
            )
            btn.grid(row=i // 2, column=i % 2, padx=6, pady=6)

        ttk.Separator(frame).grid(row=2, columnspan=2, sticky="ew", pady=8)

        # Boton para abrir una ventana nueva y añadir una cantidad de elementos
        ttk.Button(
            frame,
            text="Añadir elementos",
            command=self.abrir_anyadir_window
        ).grid(row=3, columnspan=2, pady=6)

    def mostrar_cantidad(self, product):
        cant = self.products[product]
        messagebox.showinfo(product, f"Disponemos de {cant} elementos")

    def abrir_anyadir_window(self):
        AnyadirVentana(self)


class AnyadirVentana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.title("Añadir elementos")
        self.resizable(False, False)
        self.configure(padx=12, pady=12)

        self.product_var = tk.StringVar()
        self.cant_var = tk.StringVar()

        self._crear_widgets()

    def _crear_widgets(self):
        ttk.Label(self, text="Producto").grid(row=0, column=0, sticky="w")
        product_cb = ttk.Combobox(
            self,
            textvariable=self.product_var,
            values=list(self.parent.products.keys()),
            state="readonly",
            width=18
        )
        product_cb.grid(row=1, column=0, pady=4)
        product_cb.set("Seleccione un producto")

        ttk.Label(self, text="Cantidad a añadir").grid(row=2, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(self, textvariable=self.cant_var, width=20).grid(row=3, column=0, pady=4)

        # Creación de un botón que llama a la función add_elements
        ttk.Button(
            self,
            text="Añadir",
            command=self.add_elements
        ).grid(row=4, column=0, pady=10)

    def add_elements(self):
        '''Método para añadir una cantidad de elementos a un producto
        '''
        product = self.product_var.get()
        cant = self.cant_var.get()

        if product not in self.parent.products:
            messagebox.showwarning(self, "Producto", "Seleccione un producto válido")
            return

        try:
            cant = int(cant)
        except ValueError:
            messagebox.showerror(self, "Cantidad", "Introduzca un número entero")
            return

        self.parent.products[product] += cant
        self.destroy()  # Cerramos la ventana windows

if __name__ == "__main__":
    app = ControlPanel()
    app.mainloop()
