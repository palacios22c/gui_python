# orders.py
# -*- coding: utf-8 -*-

'''
Creación de un panel de control que permita tomar órdenes/comdandas de un restaurante

El programa está compuesto por tres pestañas:
1. Order. Un panel para escribir lo que se desee
2. Currency. Selección de la divisa que se desea usar. En este ejemplo: "Euros", "Dollars", "Pounds"
3. Se muestra el mensaje de la primera pestaña y un mensaje relacionado con la divisa elegida en la segunda pestaña.
'''

# Módulos
try:
    import wx
    from wx.lib.pubsub import pub
except ImportError: 										# Error si no se encuentra el módulo
    raise(ImportError,"The wxPython module is required.")

# Variables globales
currency = 'Euros'
mss = ''

# Clase de la ventana principal
class Mywin(wx.Frame):
	def __init__(self, parent, title):
		super(Mywin, self).__init__(parent, title = title, size = (250,150))
		self.InitUI()

	def InitUI(self):
		global nb
		nb = wx.Notebook(self)				# Se usa la clase "Notebook"
		nb.AddPage(Tab1(nb),"Order")		# Primera pestaña/hoja
		nb.AddPage(Tab2(nb),"Currency")		# Segunda pestaña/hoja
		nb.AddPage(Tab3(nb),"Final")		# Tercera pestaña/hoja
		self.Centre()						# Posición de la ventana: Centro
		self.Show(True)

# Clase de la pestaña 1
class Tab1(wx.Panel):
	def __init__(self, parent):
		super(Tab1, self).__init__(parent)
		self.text = wx.TextCtrl(self, style = wx.TE_MULTILINE, size = (250,150))
		nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.Actions)

	def Actions(self, evt):
		'''Método que actualiza el texto que se escribe en la primera pestaña'''
		global mss
		mss = self.text.GetValue()
		pub.sendMessage("messenger", message = mss)	# Envíamos la información por medio de "messenger"

# Clase de la pestaña 2       
class Tab2(wx.Panel):
	def __init__(self, parent):
		super(Tab2, self).__init__(parent)
		currencies = ['Euros', 'Dollars', 'Pounds']
		self.rbox = wx.RadioBox(self, label = 'Monedas', pos = (10,10), choices = currencies,
			majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
		self.Bind(wx.EVT_RADIOBOX,self.onRadioBox)

	def onRadioBox(self,e):
		'''Método que actualiza el valor de la divisa elegida en la segunda pestaña'''
		global currency
		currency = self.rbox.GetStringSelection()

# Clase de la pestaña 3
class Tab3(wx.Panel):
	def __init__(self, parent):
		super(Tab3, self).__init__(parent)
		pub.subscribe(self.myListener, "messenger")	# Recibimos la información de "messenger"
		self.txt = wx.StaticText(self, -1, 'Your choice is Euros')

	def myListener(self, message):
		'''Método que recolecta la información de las pestañas 1 y 2 para mostrarlo en la pestaña 3'''
		msg = message
		if message:
			msg += '\n'
		msg += 'Your choice is ' + currency
		self.txt.SetLabel(msg)

### Main ###

ex = wx.App()
Mywin(None,'Orders')
ex.MainLoop()
