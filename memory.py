#memory.py
#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
This game is inspired by Simon.

The player selects how many colors will be used (from 2 to 8)
The game first shows a sequence of colors
The player try to reproduce in the same order
Each round adds a new color to the sequence (increasing the difficulty)
The player makes a mistake

Finally, a popup window shows scoring information
         and the correct color sequence
'''

# Modules
import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QLabel, QSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer

# Colors used (max 8 values) and text over these colors (black or white)
COLOR_TEXT = {
    "red": "white",
    "blue": "white",
    "green": "white",
    "purple": "white",
    "magenta": "white",
    "orange": "black",
    "yellow": "black",
    "cyan": "black"
}

# Waiting time between sequence's elements (in ms)
WAIT_TIME = 700

class MemoryGame(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Memory Game")
        self.setMinimumSize(440, 420)

        self.colors = []
        self.sequence = []
        self.user_index = 0
        self.score = 0
        self.best_score = 0

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.current_widget = None
        self.initial_screen()

    # Managing screens
    def set_screen(self, widget):
        if self.current_widget:
            self.current_widget.deleteLater()
        self.current_widget = widget
        self.main_layout.addWidget(widget)

    # Initial screen
    def initial_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Color Memory Game")                       # Title
        title.setStyleSheet("font-size: 24px; font-weight: bold") # Font style

        label = QLabel("Choose number of colors (2–8)")
        self.color_selector = QSpinBox()
        self.color_selector.setRange(2, 8)
        self.color_selector.setValue(4)                           # By default 4 colours

        start_btn = QPushButton("Start Game")
        start_btn.clicked.connect(self.start_game)

        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(QApplication.quit)

        layout.addWidget(title)
        layout.addSpacing(12)
        layout.addWidget(label)
        layout.addWidget(self.color_selector)
        layout.addSpacing(14)
        layout.addWidget(start_btn)
        layout.addWidget(exit_btn)

        self.set_screen(widget)

    # Start of the game
    def start_game(self):
        base_colors = [
            "red", "green", "blue", "yellow",
            "purple", "orange", "cyan", "magenta"
        ]

        self.colors = base_colors[:self.color_selector.value()]
        self.sequence = []
        self.user_index = 0
        self.score = 0

        self.add_random_color()
        self.game_screen()
        QTimer.singleShot(WAIT_TIME, self.play_sequence)                # Waiting time for the first element

    # Game screen
    def game_screen(self):
        widget = QWidget()
        main_layout = QVBoxLayout(widget)

        # Upper area
        self.score_label = QLabel("Score: 0")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_label.setStyleSheet("font-size: 20px; font-weight: bold") # Font style

        self.step_label = QLabel("")
        self.step_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.step_label.setStyleSheet("font-size: 14px")         # Font style

        self.info_label = QLabel("Watch the sequence")            # Message to the player
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("font-size: 18px; font-weight: 600") # Font style

        self.color_display = QLabel("")
        self.color_display.setFixedSize(260, 120)
        self.color_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.color_display.setStyleSheet("background: #ddd; border-radius: 10px")

        main_layout.addWidget(self.score_label)
        main_layout.addWidget(self.step_label)
        main_layout.addWidget(self.info_label)
        main_layout.addWidget(self.color_display, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addSpacing(12)

        # Buttons
        grid = QGridLayout()
        grid.setSpacing(8)

        self.buttons = []
        cols = 4

        for i, color in enumerate(self.colors):
            c_t = COLOR_TEXT.get(color, "black")

            btn = QPushButton(color.capitalize())
            btn.setMinimumHeight(42)
            btn.setStyleSheet(
                f"""
                background-color: {color};
                color: {c_t};
                font-weight: bold;
                """
            )
            btn.clicked.connect(lambda _, c=color: self.handle_user_input(c))
            btn.setEnabled(False)

            self.buttons.append(btn)
            grid.addWidget(btn, i // cols, i % cols)

        main_layout.addLayout(grid)
        self.set_screen(widget)

    # Sequence
    def add_random_color(self):
        self.sequence.append(random.choice(self.colors))

    def play_sequence(self):
        self.disable_buttons()
        self.info_label.setText("Watch the sequence")
        self.step = 0

        def show_next():
            if self.step < len(self.sequence):
                color = self.sequence[self.step]
                # Info "Step X/N" # To help player
                self.step_label.setText(
                    f"Step {self.step + 1} / {len(self.sequence)}"
                )
                self.color_display.setStyleSheet(
                    f"background: {color}; border-radius: 10px;"
                )
                self.step += 1
                QTimer.singleShot(WAIT_TIME, show_next)
            else:
                self.color_display.setStyleSheet(
                    "background: #ddd; border-radius: 10px;"
                )
                self.step_label.setText("")
                self.user_index = 0
                self.start_player_turn()

        QTimer.singleShot(WAIT_TIME, show_next)

    # Player's turn
    def start_player_turn(self):
        self.info_label.setText("Your turn")
        self.enable_buttons()

    def handle_user_input(self, color):
        # Show the color chosen by player
        self.color_display.setStyleSheet(
            f"background: {color}; border-radius: 10px;"
        )

        if color == self.sequence[self.user_index]:
            self.user_index += 1
            if self.user_index == len(self.sequence):
                self.score += 1
                self.score_label.setText(f"Score: {self.score}")
                self.add_random_color()
                QTimer.singleShot(WAIT_TIME, self.play_sequence)
        else:
            self.game_over()

    # Game over
    def game_over(self):
        self.best_score = max(self.best_score, self.score)

        # Pop-up with information
        QMessageBox.information(
            self,
            "Game Over",
            f"Score: {self.score}\n"
            f"Best score: {self.best_score}\n\n"
            f"Sequence:\n{', '.join(self.sequence)}"
        )
        self.initial_screen()

    # Additional methods
    def disable_buttons(self):
        for b in self.buttons:
            b.setEnabled(False)

    def enable_buttons(self):
        for b in self.buttons:
            b.setEnabled(True)

### Main ###
if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = MemoryGame()
    game.show()
    sys.exit(app.exec())
