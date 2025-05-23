from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow
from board import Board


class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        self.setWindowTitle('Chess')
        self.setFixedSize(1000, 900)
        self.move(450, 50)
        #self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.board = Board(self)
        self.board.move(100, 30)
