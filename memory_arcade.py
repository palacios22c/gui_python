#memory_arcade.py
#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Juego de memoria secuencial

El usuario elige con cuántas cartas o número quiere jugar (entre 3 y 10)
El usuario tiene que descubrir las cartas en orden, desde el 1 al número elegido
'''

# Módulos
import arcade
import random
import math
import time

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Juego de Memoria Secuencial"
CARD_SIZE = 100
CARD_GAP = 20

#   CLASE CARTA
class Card:
    def __init__(self, x, y, number):
        self.x = x
        self.y = y
        self.number = number
        self.revealed = False
        self.width = CARD_SIZE
        self.height = CARD_SIZE

        self.text = arcade.Text(
            str(self.number),
            self.x - 15,
            self.y - 20,
            arcade.color.BLACK,
            40,
            bold=True
        )

    def draw(self):
        left = self.x - self.width / 2
        right = self.x + self.width / 2
        bottom = self.y - self.height / 2
        top = self.y + self.height / 2

        color = arcade.color.WHITE if self.revealed else arcade.color.GRAY

        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, color)
        arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, arcade.color.BLACK, 3)

        if self.revealed:
            self.text.draw()

    def is_clicked(self, x, y):
        return (
            abs(x - self.x) < self.width / 2
            and abs(y - self.y) < self.height / 2
        )

#   CLASE JUEGO
class MemoryGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        self.state = "menu"   # "menu", "game", "win_wait"

        self.cards = []
        self.expected_number = 1
        self.total_numbers = 0

        self.win_timer = None

        # Texto del menú
        self.menu_line1 = arcade.Text(
            "¿Cuántos números quieres adivinar? (3 a 10)",
            100,
            SCREEN_HEIGHT - 150,
            arcade.color.WHITE,
            24
        )

        # Segundo texto del menú
        self.menu_line2 = arcade.Text(
            "Haz clic en un número.",
            100,
            SCREEN_HEIGHT - 190,
            arcade.color.WHITE,
            24
        )

        self.menu_buttons = []
        self.create_menu_buttons()

        # Texto del juego
        self.game_text = arcade.Text(
            "",
            20,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            20
        )

        # Botones superiores
        self.menu_button = arcade.Text(
            "Menú",
            SCREEN_WIDTH - 200,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            20
        )

        self.exit_button = arcade.Text(
            "Salir",
            SCREEN_WIDTH - 100,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            20
        )

    #   MENÚ INICIAL
    def create_menu_buttons(self):
        x_start = 150
        y = SCREEN_HEIGHT // 2

        for i in range(3, 11):
            x = x_start + (i - 3) * 60
            self.menu_buttons.append((i, x, y))

    def draw_menu(self):
        self.menu_line1.draw()
        self.menu_line2.draw()

        for number, x, y in self.menu_buttons:
            left = x - 25
            right = x + 25
            bottom = y - 25
            top = y + 25

            arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, arcade.color.LIGHT_BLUE)
            arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, arcade.color.BLACK, 3)

            arcade.Text(str(number), x - 10, y - 12, arcade.color.BLACK, 20).draw()

    #   CREAR GRID DE CARTAS
    def setup_game(self):
        self.cards = []
        self.expected_number = 1

        numbers = list(range(1, self.total_numbers + 1))
        random.shuffle(numbers)

        cols = math.ceil(math.sqrt(self.total_numbers))
        rows = math.ceil(self.total_numbers / cols)

        grid_width = cols * CARD_SIZE + (cols - 1) * CARD_GAP
        grid_height = rows * CARD_SIZE + (rows - 1) * CARD_GAP

        start_x = (SCREEN_WIDTH - grid_width) / 2 + CARD_SIZE / 2
        start_y = (SCREEN_HEIGHT - grid_height) / 2 + CARD_SIZE / 2

        index = 0
        for row in range(rows):
            for col in range(cols):
                if index >= self.total_numbers:
                    break

                x = start_x + col * (CARD_SIZE + CARD_GAP)
                y = start_y + row * (CARD_SIZE + CARD_GAP)

                self.cards.append(Card(x, y, numbers[index]))
                index += 1

        self.game_text.text = f"Siguiente número: {self.expected_number}"

    #   DIBUJAR
    def on_draw(self):
        self.clear()

        if self.state == "menu":
            self.draw_menu()

        elif self.state == "game":
            for card in self.cards:
                card.draw()

            self.game_text.draw()
            self.menu_button.draw()
            self.exit_button.draw()

        elif self.state == "win_wait":
            for card in self.cards:
                card.draw()

            arcade.Text(
                "¡Has ganado!",
                SCREEN_WIDTH / 2 - 80,
                SCREEN_HEIGHT - 80,
                arcade.color.BLACK,
                30
            ).draw()

    #   CLIC DEL RATÓN
    def on_mouse_press(self, x, y, button, modifiers):

        # --- MENÚ ---
        if self.state == "menu":
            for number, bx, by in self.menu_buttons:
                if abs(x - bx) < 25 and abs(y - by) < 25:
                    self.total_numbers = number
                    self.state = "game"
                    self.setup_game()
            return

        # --- BOTÓN MENÚ ---
        if self.state == "game":
            if SCREEN_WIDTH - 200 < x < SCREEN_WIDTH - 140 and SCREEN_HEIGHT - 50 < y < SCREEN_HEIGHT - 10:
                self.state = "menu"
                return

        # --- BOTÓN SALIR ---
        if self.state == "game":
            if SCREEN_WIDTH - 120 < x < SCREEN_WIDTH - 40 and SCREEN_HEIGHT - 50 < y < SCREEN_HEIGHT - 10:
                self.close()   # Cerrar
                return

        # --- JUEGO ---
        if self.state == "game":
            for card in self.cards:
                if card.is_clicked(x, y):
                    self.handle_card_click(card)

    #   LÓGICA DEL JUEGO
    def handle_card_click(self, card):
        if card.number == self.expected_number:
            card.revealed = True
            self.expected_number += 1

            self.game_text.text = f"Siguiente número: {self.expected_number}"

            # Esperamos 1 segundo
            if self.expected_number > len(self.cards):
                self.state = "win_wait"
                self.win_timer = time.time()
                return

        else:
            for c in self.cards:
                c.revealed = False
            self.expected_number = 1
            self.game_text.text = f"Siguiente número: {self.expected_number}"

    #   UPDATE (temporizador)
    def on_update(self, delta_time):
        if self.state == "win_wait":
            if time.time() - self.win_timer >= 1:
                self.setup_game()
                self.state = "game"

#   MAIN
def main():
    game = MemoryGame()
    arcade.run()

if __name__ == "__main__":
    main()
