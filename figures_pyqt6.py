#figures_pyqt6.py
#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
On the canvas, the user draws a square, a triangle, or a circle
Each figure is positioned randomly on the canvas
The user can move the last inserted figure with the mouse
There is a button that deletes the last figure
The light/dark mode and the language (Spanish/English) can be switched

En el canvas se va dibujando un cuadrado, un triángulo o un círculo a elección del usuario
Cada una de las figuras se posiciona de forma aleatoria en el canvas
El usuario puede mover con el ratón la última figura introducida
Hay un botón que borra la última figura
Se puede cambiar el modo claro/oscuro y el idioma a español/inglés
'''

# Modules
import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QMenuBar, QMenu
)
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QAction
from PyQt6.QtCore import Qt, QRectF, QPointF

# Class Drawing Canvas
class DrawingCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.shapes = [] # Figures on the canvas
        self.dragging = False
        self.drag_offset = None
        self.setStyleSheet("""
            background-color: white;
            border: 1px solid #CCCCCC;
        """)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for shape in self.shapes:
            shape_type, rect, color = shape

            painter.setPen(QPen(Qt.GlobalColor.black, 2))
            painter.setBrush(QBrush(color))

            if shape_type in ("square", "rectangle"):
                painter.drawRect(rect)
            elif shape_type == "triangle":
                p1 = QPointF(rect.x(), rect.y() + rect.height())
                p2 = QPointF(rect.x() + rect.width(), rect.y() + rect.height())
                p3 = QPointF(rect.x() + rect.width() / 2, rect.y())
                painter.drawPolygon(p1, p2, p3)

    def add_shape(self, shape_type):
        w, h = self.width(), self.height()
        if w <= 0 or h <= 0:
            w, h = 600, 400

        size = random.randint(40, 120)
        x = random.randint(10, max(10, int(w - size - 10)))
        y = random.randint(10, max(10, int(h - size - 10)))

        if shape_type == "rectangle":
            width = size * random.uniform(1.2, 2.0)
            height = size
        else:
            width = height = size

        rect = QRectF(x, y, width, height)

        color = QColor(
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )

        self.shapes.append((shape_type, rect, color))
        self.update()

    def remove_last(self):
        if self.shapes:
            self.shapes.pop()
            self.update()

    def mousePressEvent(self, event):
        if not self.shapes:
            return

        shape_type, rect, color = self.shapes[-1]
        if rect.contains(event.position()):
            self.dragging = True
            self.drag_offset = event.position() - rect.topLeft()

    def mouseMoveEvent(self, event):
        if self.dragging and self.shapes:
            shape_type, rect, color = self.shapes[-1]
            new_x = event.position().x() - self.drag_offset.x()
            new_y = event.position().y() - self.drag_offset.y()
            rect.moveTo(new_x, new_y)
            self.shapes[-1] = (shape_type, rect, color)
            self.update()

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.drag_offset = None


# Main Window
class ShapeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dibujar Figuras - PyQt6")
        self.setMinimumSize(1000, 700)

        self.canvas = DrawingCanvas()
        self.dark_mode = False
        self.language = "es"

        self.build_ui()
        self.apply_light_mode()

    def build_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Menu
        menu_bar = QMenuBar()

        file_menu = QMenu("Archivo", self)
        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        options_menu = QMenu("Opciones", self)

        # Toggle dark/light mode
        self.toggle_dark_action = QAction("Cambiar modo oscuro/claro", self)
        self.toggle_dark_action.triggered.connect(self.toggle_dark_mode)
        options_menu.addAction(self.toggle_dark_action)

        # Toggle language
        self.toggle_lang_action = QAction("Cambiar idioma", self)
        self.toggle_lang_action.triggered.connect(self.toggle_language)
        options_menu.addAction(self.toggle_lang_action)

        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(options_menu)

        main_layout.addWidget(menu_bar)

        # Buttons
        self.btn_square = QPushButton("Cuadrado")
        self.btn_triangle = QPushButton("Triángulo")
        self.btn_rectangle = QPushButton("Rectángulo")
        self.btn_delete = QPushButton("Borrar Última")

        self.btn_square.clicked.connect(lambda: self.canvas.add_shape("square"))
        self.btn_triangle.clicked.connect(lambda: self.canvas.add_shape("triangle"))
        self.btn_rectangle.clicked.connect(lambda: self.canvas.add_shape("rectangle"))
        self.btn_delete.clicked.connect(self.canvas.remove_last)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10, 5, 10, 5)
        button_layout.setSpacing(10)
        button_layout.addWidget(self.btn_square)
        button_layout.addWidget(self.btn_triangle)
        button_layout.addWidget(self.btn_rectangle)
        button_layout.addWidget(self.btn_delete)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        main_layout.addWidget(self.canvas, stretch=1)

        self.setLayout(main_layout)

    # Toggle language
    def toggle_language(self):
        self.language = "en" if self.language == "es" else "es"

        if self.language == "es":
            self.btn_square.setText("Cuadrado")
            self.btn_triangle.setText("Triángulo")
            self.btn_rectangle.setText("Rectángulo")
            self.btn_delete.setText("Borrar Última")
            self.setWindowTitle("Dibujar Figuras")
            self.toggle_lang_action.setText("Cambiar idioma")
            self.toggle_dark_action.setText("Cambiar modo oscuro/claro")
        else:
            self.btn_square.setText("Square")
            self.btn_triangle.setText("Triangle")
            self.btn_rectangle.setText("Rectangle")
            self.btn_delete.setText("Delete Last")
            self.setWindowTitle("Draw Shapes")
            self.toggle_lang_action.setText("Change language")
            self.toggle_dark_action.setText("Toggle dark/light mode")

    # Toggle dark/light mode
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.apply_dark_mode()
        else:
            self.apply_light_mode()

    def apply_dark_mode(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #222;
                color: white;
            }
            QPushButton {
                background-color: #444;
                color: white;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QMenuBar {
                background-color: #333;
                color: white;
            }
            QMenu {
                background-color: #333;
                color: white;
            }
        """)
        self.canvas.setStyleSheet("""
            background-color: #111;
            border: 1px solid #555;
        """)

    def apply_light_mode(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                color: black;
            }
            QPushButton {
                background-color: #DDD;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #CCC;
            }
            QMenuBar {
                background-color: #EEE;
                color: black;
            }
            QMenu {
                background-color: #EEE;
                color: black;
            }
        """)
        self.canvas.setStyleSheet("""
            background-color: white;
            border: 1px solid #CCCCCC;
        """)


# Main app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShapeApp()
    window.show()
    sys.exit(app.exec())
