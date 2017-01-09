# gamePPT_kivy.py
# -*- coding: utf-8 -*-

'''
El juego "Piedra, papel o tijera" utilizando Kivy

El usuario puede elegir una de las opciones (piedra, papel o tijera) desde uno de los tres botones.
Una vez pulsado el ordenador devuelve un mensaje por consola informando si ha ganado, empatado o perdido.
Finalmente está el botón para salir.
'''

# Módulos
import kivy
#kivy.require("1.9.1") # This program was created using this version. It could work with previous versions

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from functools import partial
from random import randint

# Global values
# RGB (used as background buttons)
rojo = [1,0,0,1]
verde = [0,1,0,1]
azul =  [0,0,1,1]

jugadas = ['Piedra', 'Papel', 'Tijera']

# Game class
class gamePPT(App): # Juego Piedra, Papel o Tijeras

    def game(self, *args):
    	'''Método que realiza el juego, devolviendo un mensaje de salida'''
        rival = randint(0,2)						# Se elige al azar un valor entero entre 0 y 2
        resultado = args[0]*args[0] - rival*rival 	# (diferencia de cuadrados)

        if resultado == 0:							# Tie
            print('Empate. Ambos han elegido ' + jugadas[args[0]])
        elif resultado in (-4,1,3):					# Player wins. (-4, 1, 3) are known values for prior experience
            print('Has ganado. Has elegido ' + jugadas[args[0]] + ' y el rival ' + jugadas[rival])
        else:										# Computer wins. (-3, -1, 4) are known values for prior experience
            print('Has perdido. Has elegido ' + jugadas[args[0]] + ' y el rival ' + jugadas[rival])

    def build(self):
    	'''Construcción de los botones y las acciones asociadas'''
        layout = BoxLayout(padding=10, orientation="vertical")
    	
    	# Creation of buttons
        btn1 = Button(text="Piedra", background_color=rojo)
        btn2 = Button(text="Papel", background_color=verde)
        btn3 = Button(text="Tijera", background_color=azul)

        # Associated actions to every button
        buttoncallback = partial(self.game, 0)
        btn1.bind(on_press=buttoncallback)
        buttoncallback = partial(self.game, 1)
        btn2.bind(on_press=buttoncallback)
        buttoncallback = partial(self.game, 2)
        btn3.bind(on_press=buttoncallback)

        # Buttons are put in their places
        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout.add_widget(btn3)

        # Last button: Exit button
        btn = Button(text='Salir',
                        size_hint=(.5, .5),
                        pos_hint={'center_x': .5, 'center_y': .5})
        btn.bind(on_press=App.get_running_app().stop)
        layout.add_widget(btn)
        return layout

### Main ###

if __name__ == "__main__":
    myApp = gamePPT()
    myApp.run()
