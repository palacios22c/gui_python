#memory_tk.py
#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
This game is inspired by Simon.
Multilingual version

The game first shows a sequence of colors
The player try to reproduce in the same order
Each round adds a new color to the sequence (increasing the difficulty)
The player makes a mistake

Finally, a message shows the correct last color
'''

# Modules
import tkinter as tk
import random
import time
import threading

# Colors
COLORS = {
    "green": "#00A74A",
    "red": "#9F0F17",
    "yellow": "#CCA707",
    "blue": "#094A8F",
}

# Bright colors
BRIGHT = {
    "green": "#00FF7F",
    "red": "#FF4C4C",
    "yellow": "#FFFF66",
    "blue": "#4C8CFF",
}

# Name of colors in Spanish and English
COLOR_NAMES = {
    "es": {
        "green": "VERDE",
        "red": "ROJO",
        "yellow": "AMARILLO",
        "blue": "AZUL",
    },
    "en": {
        "green": "GREEN",
        "red": "RED",
        "yellow": "YELLOW",
        "blue": "BLUE",
    },
    "it": {
        "green": "VERDE",
        "red": "ROSSO",
        "yellow": "GIALLO",
        "blue": "BLU",
    },
    "pt": {
        "green": "VERDE",
        "red": "VERMELHO",
        "yellow": "AMARELO",
        "blue": "AZUL",
    }
}

# Messages and their translation
TEXT = {
    "es": {
        "start": "Iniciar",
        "try_again": "Reintentar",
        "watch": "Observa la secuencia...",
        "your_turn": "Tu turno: repite la secuencia",
        "good": "¡Bien hecho!",
        "score": "Puntuación",
        "game_over": "Fin del juego",
        "correct_color": "El color correcto era:",
        "language": "Idioma",
    },
    "en": {
        "start": "Start",
        "try_again": "Try Again",
        "watch": "Watch the sequence...",
        "your_turn": "Your turn: repeat the sequence",
        "good": "Well done!",
        "score": "Score",
        "game_over": "Game Over",
        "correct_color": "The correct color was:",
        "language": "Language",
    },
    "it": {
        "start": "Inizia",
        "try_again": "Riprova",
        "watch": "Guarda la sequenza…",
        "your_turn": "Il tuo turno: ripeti la sequenza",
        "good": "Ben fatto!",
        "score": "Punteggio",
        "game_over": "Fine del gioco",
        "correct_color": "Il colore corretto era:",
        "language": "Lingua",
    },
    "pt": {
        "start": "Iniciar",
        "try_again": "Tentar novamente",
        "watch": "Observe a sequência…",
        "your_turn": "Sua vez: repita a sequência",
        "good": "Muito bem!",
        "score": "Pontuação",
        "game_over": "Fim de jogo",
        "correct_color": "A cor correta era:",
        "language": "Idioma",
    }
}

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Game")

        # Minimum size and resizable window
        self.root.minsize(350, 580)
        self.root.resizable(True, True)

        # Default language
        self.lang = "en"

        self.sequence = []
        self.user_index = 0
        self.is_playing = False
        self.score = 0

        # Select a language
        self.lang_var = tk.StringVar(value="es")
        lang_frame = tk.Frame(root)
        lang_frame.pack(pady=5)

        self.lang_label = tk.Label(lang_frame, text="")
        self.lang_label.pack(side="left", padx=5)

        self.radio_es = tk.Radiobutton(
            lang_frame, text="Español",
            variable=self.lang_var, value="es",
            command=self.apply_language
        )
        self.radio_en = tk.Radiobutton(
            lang_frame, text="English",
            variable=self.lang_var, value="en",
            command=self.apply_language
        )
        self.radio_it = tk.Radiobutton(
            lang_frame, text="Italiano",
            variable=self.lang_var, value="it",
            command=self.change_language
        )
        self.radio_pt = tk.Radiobutton(
            lang_frame, text="Português",
            variable=self.lang_var, value="pt",
            command=self.change_language
        )

        self.radio_es.pack(side="left")
        self.radio_en.pack(side="left")
        self.radio_it.pack(side="left")
        self.radio_pt.pack(side="left")

        # Buttons
        self.buttons = {}
        self.create_buttons()

        # Score
        self.score_label = tk.Label(root, text="", font=("Arial", 16))
        self.score_label.pack(pady=10)

        # Status
        self.status_label = tk.Label(root, text="", font=("Arial", 14))
        self.status_label.pack(pady=5)

        # Second line of (game over) status
        self.correct_label = tk.Label(root, text="", font=("Arial", 14))
        self.correct_label.pack(pady=5)

        # Start button
        self.start_button = tk.Button(
            root, text="", font=("Arial", 16),
            command=self.start_game
        )
        self.start_button.pack(pady=20)

        # Apply language
        self.apply_language()

    def apply_language(self):
        self.lang = self.lang_var.get()
        self.start_button.config(text=TEXT[self.lang]["start"])
        self.lang_label.config(text=f"{TEXT[self.lang]['language']}:")
        self.update_score()

    def disable_language_selector(self):
        '''Disable selector when the game is on'''
        self.radio_es.config(state="disabled")
        self.radio_en.config(state="disabled")

    def enable_language_selector(self):
        '''Enable selector when the game has started or over'''
        self.radio_es.config(state="normal")
        self.radio_en.config(state="normal")

    def create_buttons(self):
        '''Create buttons'''
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        for i in range(2):
            frame.rowconfigure(i, weight=1)
            frame.columnconfigure(i, weight=1)

        self.buttons["green"] = tk.Button(
            frame, bg=COLORS["green"],
            command=lambda: self.user_press("green")
        )
        self.buttons["red"] = tk.Button(
            frame, bg=COLORS["red"],
            command=lambda: self.user_press("red")
        )
        self.buttons["yellow"] = tk.Button(
            frame, bg=COLORS["yellow"],
            command=lambda: self.user_press("yellow")
        )
        self.buttons["blue"] = tk.Button(
            frame, bg=COLORS["blue"],
            command=lambda: self.user_press("blue")
        )

        # Set buttons on grid
        self.buttons["green"].grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.buttons["red"].grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.buttons["yellow"].grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.buttons["blue"].grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

    # Start of the game
    def start_game(self):
        if self.is_playing:
            return

        self.sequence = []
        self.user_index = 0
        self.score = 0
        self.update_score()
        self.status_label.config(text="")
        self.correct_label.config(text="")
        self.is_playing = True

        # Enable language selector
        self.enable_language_selector()
        self.next_round()

    def update_score(self):
        self.score_label.config(text=f"{TEXT[self.lang]['score']}: {self.score}")

    def next_round(self):
        self.user_index = 0
        self.sequence.append(random.choice(list(COLORS.keys()))) # random color to use
        self.score = len(self.sequence) - 1
        self.update_score()

        self.status_label.config(text=TEXT[self.lang]["watch"], fg="black")
        self.correct_label.config(text="")

        # Enable language selector
        self.enable_language_selector()

        threading.Thread(target=self.play_sequence).start()

    def play_sequence(self):
        # Disable language selector
        self.disable_language_selector()

        time.sleep(1) # Waiting time
        for color in self.sequence:
            self.flash(color)
            time.sleep(0.5)

        self.status_label.config(text=TEXT[self.lang]["your_turn"], fg="blue")

    def flash(self, color):
        btn = self.buttons[color]
        btn.config(bg=BRIGHT[color])
        self.root.update()
        time.sleep(0.3) # Time to change from bright into normal color
        btn.config(bg=COLORS[color])
        self.root.update()

    def user_press(self, color):
        if not self.is_playing:
            # User is not playing right now
            return

        self.flash(color)

        if color == self.sequence[self.user_index]:
            # Right color
            self.user_index += 1
            if self.user_index == len(self.sequence):
                self.status_label.config(text=TEXT[self.lang]["good"], fg="green")
                self.root.after(600, self.next_round)
        else:
            self.game_over(correct_color=self.sequence[self.user_index])

    # Game over
    def game_over(self, correct_color):
        self.is_playing = False # User is not playing right now
        self.start_button.config(text=TEXT[self.lang]["try_again"])

        # First line: Game Over / Fin del juego
        self.status_label.config(
            text=TEXT[self.lang]["game_over"],
            fg="red"
        )

        # Second line of Game Over message
        translated = COLOR_NAMES[self.lang][correct_color]
        self.correct_label.config(
            text=f"{TEXT[self.lang]['correct_color']} {translated}",
            fg="red"
        )

        self.flash_all() # All colours are flashing after losing

        # Enable language selector
        self.enable_language_selector()

    def flash_all(self):
        '''All colours are flashing after losing'''
        for _ in range(2):
            for color in COLORS:
                self.buttons[color].config(bg=BRIGHT[color])
            self.root.update()
            time.sleep(0.3)
            for color in COLORS:
                self.buttons[color].config(bg=COLORS[color])
            self.root.update()
            time.sleep(0.3)

### Main ###
if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
