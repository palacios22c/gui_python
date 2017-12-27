# figures_wx.py
# -*- coding: utf-8 -*-

'''
Ejemplo de figuras

Se ha usado wxPython como módulo para crear el canvas y dibujar tres figuras
'''

# Módulo wxPython
try:
    import wx
except ImportError: 										                            # Error si no se encuentra el módulo
    raise(ImportError,"The wxPython module is required.")

class View(wx.Panel):
    def __init__(self, parent):
        super(View, self).__init__(parent)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
    def on_size(self, event):
        event.Skip()
        self.Refresh()
    def on_paint(self, event):
        w, h = 500, 500                                                                 # Valores para ser usados (width = height = 250)
        self.SetClientSize((w, h))                                                      # Tamaño del canvas
        self.Center()                                                                   # Canvas centrado

        # Figuras
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 2))                                                  # Líneas negras
        dc.SetBrush(wx.Brush(wx.BLACK))                                                 # Relleno negro
        dc.DrawRectangle(w / 4, h / 4, w / 2, h / 2)                                    # Rectángulo/Cuadrado
        dc.SetBrush(wx.Brush(wx.YELLOW))                                                # Relleno amarillo
        dc.DrawCircle(w / 2, h / 2, min(w,h)/4)                                         # Círculo
        dc.SetBrush(wx.Brush(wx.GREEN))                                                 # Relleno verde
        dc.DrawPolygon([wx.Point(w/4, h/4), wx.Point(w/2, h/2), wx.Point(w/4, h*3/4)])  # Triángulo

class Frame(wx.Frame):
    def __init__(self):
        super(Frame, self).__init__(None)

        self.SetTitle("Figures")							                            # Título de la ventana
        self.Center()                                                                   # Centrado de la ventana
        self.CreateStatusBar()								                            # Barra de estado

        # MENU
        filemenu= wx.Menu()

        # wx.ID_ABOUT, wx.ID_EXIT son IDs estandar de wxPython
        aboutitem = filemenu.Append(wx.ID_NEW, "&About"," Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutitem)
        filemenu.AppendSeparator()
        quititem = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnQuit, quititem)

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        self.SetMenuBar(menuBar)
        self.view = View(self)
        self.Show(True)

    def OnQuit(self, e):
        '''Cerrar la aplicación'''
        self.Close()

    def OnAbout(self, e):
        '''Ventana de información'''
        dlg = wx.MessageDialog(None, "Figures example", "About...", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

# MAIN
def main():
    app = wx.App(False)
    frame = Frame()
    frame.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()