# memory_pairs.py
# -*- coding: utf-8 -*-

'''
Juego de memoria desarrollado con pyglet.

El jugador debe encontrar todas las parejas de cartas volteando dos a la vez.
Incluye selección de dificultad

Memory Match Game built with pyglet.

The player must flip two cards at a time to find matching emoji pairs.
The game includes multiple difficulty levels
'''
import random
import pyglet
from pyglet import shapes

# Constants
BASE_CARD_SIZE = 90
PADDING = 20

# Emojis
SYMBOLS = [
    "🍎","🍌","🍇","🍉","🍒","🍍","🥝","🍑",
    "🍋","🥥","🍈","🍐","🍓","🥭","🍆","🥑",
    "🍔","🍟","🍕","🌭","🍿","🧁","🍪","🍩",
    "🐶","🐱","🐭","🐹","🐰","🦊","🐻","🐼",
    "🐨","🐯","🦁","🐮","🐷","🐸","🐵","🐔"
]


# Button class
class Button:
    def __init__(self, x, y, w, h, text, batch, on_click, color=(50, 120, 200)):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.on_click = on_click

        self.rect = shapes.Rectangle(
            x - w/2, y - h/2, w, h,
            color=color,
            batch=batch
        )

        self.label = pyglet.text.Label(
            text,
            font_size=20,
            x=x, y=y,
            anchor_x="center", anchor_y="center",
            batch=batch
        )

    def contains(self, px, py):
        return (
            self.x - self.w/2 <= px <= self.x + self.w/2 and
            self.y - self.h/2 <= py <= self.y + self.h/2
        )


# Card class
class Card:
    def __init__(self, x, y, size, symbol, batch):
        self.x, self.y = x, y
        self.size = size
        self.symbol = symbol
        self.revealed = False
        self.matched = False

        self.rect = shapes.Rectangle(
            x - size/2, y - size/2,
            size, size,
            color=(20, 80, 180),
            batch=batch
        )
        self.label = pyglet.text.Label(
            "",
            font_size=int(size * 0.45),
            x=x, y=y,
            anchor_x="center", anchor_y="center",
            batch=batch
        )

    def draw(self):
        if self.revealed or self.matched:
            self.rect.color = (200, 120, 40)
            self.label.text = self.symbol
        else:
            self.rect.color = (20, 80, 180)
            self.label.text = "?"

    def contains(self, px, py):
        return (
            self.x - self.size/2 <= px <= self.x + self.size/2 and
            self.y - self.size/2 <= py <= self.y + self.size/2
        )

# Main window
class MemoryWindow(pyglet.window.Window):
    def __init__(self):
        # First window
        super().__init__(800, 600, "Juego de Memoria (pyglet)", resizable=False)
        pyglet.gl.glClearColor(0.05, 0.05, 0.15, 1)

        self.state = "menu"
        self.batch = pyglet.graphics.Batch()
        self.cards = []
        self.buttons = []

        self.rows = 4
        self.cols = 4

        self.first_card = None
        self.second_card = None
        self.locked = False
        self.pairs_found = 0

        self.status_label = pyglet.text.Label(
            "",
            font_size=22,
            x=self.width // 2,
            y=self.height - 40,
            anchor_x="center",
            anchor_y="center",
            color=(255, 255, 255, 255)
        )

        self.build_menu()

    def adjust_window(self):
    '''Adjusting window according to screen size'''

        # Size of current screen
        screen = self.screen

        max_w = screen.width - 100
        max_h = screen.height - 100

        # Ideal size according to number of columns and rows
        ideal_w = self.cols * (self.card_size + PADDING) + 200
        ideal_h = self.rows * (self.card_size + PADDING) + 250

        # Final size
        final_w = min(ideal_w, max_w)
        final_h = min(ideal_h, max_h)

        self.set_size(int(final_w), int(final_h))

        # Window position
        self.set_location(
            (screen.width - final_w) // 2,
            (screen.height - final_h) // 2
        )

        # Info message (label), upper side
        self.status_label.x = self.width // 2
        self.status_label.y = self.height - 40

    # Main menu
    def build_menu(self):
        self.state = "menu"
        self.batch = pyglet.graphics.Batch()
        self.buttons = []

        pyglet.text.Label(
            "Selecciona dificultad",
            font_size=32,
            x=self.width//2,
            y=self.height - 150,
            anchor_x="center", anchor_y="center",
            color=(255, 255, 0, 255),
            batch=self.batch
        )

        def add_button(text, y, rows, cols):
            self.buttons.append(
                Button(
                    self.width//2, y, 250, 60,
                    text, self.batch,
                    lambda: self.start_game(rows, cols)
                )
            )

        add_button("Fácil (4x4)", 370, 4, 4)
        add_button("Medio (6x6)", 270, 6, 6)
        add_button("Difícil (8x8)", 170, 8, 8)

        # Botón salir
        self.buttons.append(
            Button(
                self.width // 2, 40, 250, 60,
                "Salir",
                self.batch,
                lambda: pyglet.app.exit(),
                color=(200, 60, 60)
            )
        )

    # Start game
    def start_game(self, rows, cols):
        self.rows, self.cols = rows, cols

        # Escalar cartas si el tablero es grande
        self.card_size = BASE_CARD_SIZE
        if rows >= 6 or cols >= 6:
            self.card_size = 70
        if rows >= 8 or cols >= 8:
            self.card_size = 55

        self.adjust_window()
        self.setup_board()
        self.state = "game"

    # Board
    def setup_board(self):
        self.batch = pyglet.graphics.Batch()
        self.cards = []
        self.buttons = []

        total_cards = self.rows * self.cols
        pairs = total_cards // 2

        # Emojis for this round
        chosen = random.sample(SYMBOLS, pairs)
        deck = chosen * 2
        random.shuffle(deck)

        self.first_card = None
        self.second_card = None
        self.locked = False
        self.pairs_found = 0
        self.status_label.text = "Encuentra todas las parejas"

        start_x = (self.width - (self.cols * self.card_size + (self.cols - 1) * PADDING)) / 2 + self.card_size/2
        start_y = self.height - 150

        index = 0
        for r in range(self.rows):
            for c in range(self.cols):
                x = start_x + c * (self.card_size + PADDING)
                y = start_y - r * (self.card_size + PADDING)
                self.cards.append(Card(x, y, self.card_size, deck[index], self.batch))
                index += 1

        # Reset button
        self.buttons.append(
            Button(
                self.width//2, 80, 200, 50,
                "Reiniciar",
                self.batch,
                self.setup_board
            )
        )

        # Menu button
        self.buttons.append(
            Button(
                self.width//2, 20, 200, 50,
                "Menú",
                self.batch,
                self.build_menu
            )
        )

    # Draw
    def on_draw(self):
        self.clear()

        if self.state == "menu":
            self.batch.draw()
            return

        for card in self.cards:
            card.draw()

        self.batch.draw()
        self.status_label.draw()

    # Mouse click
    def on_mouse_press(self, x, y, button, modifiers):
        for b in self.buttons:
            if b.contains(x, y):
                b.on_click()
                return

        if self.state != "game" or self.locked:
            return

        for card in self.cards:
            if card.contains(x, y) and not card.revealed and not card.matched:
                card.revealed = True

                if not self.first_card:
                    self.first_card = card
                elif not self.second_card:
                    self.second_card = card
                    self.locked = True
                    pyglet.clock.schedule_once(self.check_pair, 0.8)
                break

    # Check emoji pair
    def check_pair(self, dt):
        if self.first_card.symbol == self.second_card.symbol:
            self.first_card.matched = True
            self.second_card.matched = True
            self.pairs_found += 1
            self.status_label.text = f"Parejas encontradas: {self.pairs_found}"
        else:
            self.first_card.revealed = False
            self.second_card.revealed = False

        self.first_card = None
        self.second_card = None
        self.locked = False

# Main app
if __name__ == "__main__":
    MemoryWindow()
    pyglet.app.run()
