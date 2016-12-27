# pcontrol_kivy.py
# -*- coding: utf-8 -*-

import kivy
#kivy.require("1.9.1") # This program was created using this version. It could work with previous versions

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from functools import partial
from random import randint

rojo = [1,0,0,1]
verde = [0,1,0,1]
azul =  [0,0,1,1]

jugadas = ['Piedra', 'Papel', 'Tijera']

class gamePPT(App): # Juego Piedra, Papel o Tijeras

    def game(self, *args):
        rival = randint(0,2)
        resultado = args[0]*args[0] - rival*rival # (diferencia de cuadrados)

        if resultado == 0:
            print('Empate. Ambos han elegido ' + jugadas[args[0]])
        elif resultado in (-4,1,3):
            print('Has ganado. Has elegido ' + jugadas[args[0]] + ' y el rival ' + jugadas[rival])
        else:
            print('Has perdido. Has elegido ' + jugadas[args[0]] + ' y el rival ' + jugadas[rival])

    def build(self):
        layout = BoxLayout(padding=10, orientation="vertical")
    
        btn1 = Button(text="Piedra", background_color=rojo)
        btn2 = Button(text="Papel", background_color=verde)
        btn3 = Button(text="Tijera", background_color=azul)

        buttoncallback = partial(self.game, 0)
        btn1.bind(on_press=buttoncallback)
        buttoncallback = partial(self.game, 1)
        btn2.bind(on_press=buttoncallback)
        buttoncallback = partial(self.game, 2)
        btn3.bind(on_press=buttoncallback)

        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout.add_widget(btn3)

        btn = Button(text='Salir',
                        size_hint=(.5, .5),
                        pos_hint={'center_x': .5, 'center_y': .5})
        btn.bind(on_press=App.get_running_app().stop)
        layout.add_widget(btn)
        return layout

if __name__ == "__main__":
    myApp = gamePPT()
    myApp.run()
