from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel
from PyQt6.QtGui import QFont
from board import Board


class Window(QWidget):
    def __init__(self):
        super().__init__(parent=None)

        self.setFixedSize(880, 740)
        self.move(450, 50)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet('color: #FFF;')

        font = QFont('Arial', 12, QFont.Weight.Bold)

        self.background = QWidget(self)
        self.background.setFixedSize(self.size())
        self.background.setStyleSheet('background-color: #313439; border-radius: 10px; border-top-left-radius: 15px; border-top-right-radius: 15px;')

        self.title_bar = QLabel(self)
        self.title_bar.setFixedSize(self.width(), 40)
        self.title_bar.setStyleSheet('background-color: #28292E; border-top-left-radius: 10px; border-top-right-radius: 10px;')

        self.title = QLabel(self)
        self.title.setText('Find The Best Move')
        self.title.setFixedSize(200, 40)
        self.title.move(30, 0)
        self.title.setFont(font)

        self.button_close = QPushButton(self)
        self.button_close.setFixedSize(14, 14)
        self.button_close.move(850, 13)
        self.button_close.clicked.connect(self.close)
        self.button_close.setStyleSheet('background-color: #FF5953; border-radius: 7px;')
        self.button_close.setCursor(Qt.CursorShape.PointingHandCursor)

        self.button_minimize = QPushButton(self)
        self.button_minimize.setFixedSize(14, 14)
        self.button_minimize.move(829, 13)
        self.button_minimize.clicked.connect(self.showMinimized)
        self.button_minimize.setStyleSheet('background-color: #EBC631; border-radius: 7px;')
        self.button_minimize.setCursor(Qt.CursorShape.PointingHandCursor)

        self.board = Board(self)
        self.board.move(30, 70)

        self.engine_evaluation = QLabel(self)
        self.engine_evaluation.setFixedSize(150, 80)
        self.engine_evaluation.move(700, 70)
        self.engine_evaluation.setStyleSheet('background-color: #28292E; border-radius: 15px')
        self.engine_evaluation.setText('+0.37')
        self.engine_evaluation.setFont(QFont('Arial', 25, QFont.Weight.Bold))
        self.engine_evaluation.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.engine_move_1 = QLabel(self)
        self.engine_move_1.setFixedSize(150, 50)
        self.engine_move_1.move(700, 165)
        self.engine_move_1.setStyleSheet('background-color: #28292E; border-radius: 10px')
        self.engine_move_1.setText('Qxb5 (+0.37)')
        self.engine_move_1.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        self.engine_move_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.engine_move_2 = QLabel(self)
        self.engine_move_2.setFixedSize(150, 50)
        self.engine_move_2.move(700, 220)
        self.engine_move_2.setStyleSheet('background-color: #28292E; border-radius: 10px')
        self.engine_move_2.setText('Nc3 (+0.32)')
        self.engine_move_2.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        self.engine_move_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.engine_move_3 = QLabel(self)
        self.engine_move_3.setFixedSize(150, 50)
        self.engine_move_3.move(700, 275)
        self.engine_move_3.setStyleSheet('background-color: #28292E; border-radius: 10px')
        self.engine_move_3.setText('Bg5 (+0.21)')
        self.engine_move_3.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        self.engine_move_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.engine_move_4 = QLabel(self)
        self.engine_move_4.setFixedSize(150, 50)
        self.engine_move_4.move(700, 330)
        self.engine_move_4.setStyleSheet('background-color: #28292E; border-radius: 10px')
        self.engine_move_4.setText('O-O (+0.19)')
        self.engine_move_4.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        self.engine_move_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.engine_move_5 = QLabel(self)
        self.engine_move_5.setFixedSize(150, 50)
        self.engine_move_5.move(700, 385)
        self.engine_move_5.setStyleSheet('background-color: #28292E; border-radius: 10px')
        self.engine_move_5.setText('a3 (+0.01)')
        self.engine_move_5.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        self.engine_move_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_turn = QLabel(self)
        self.label_turn.setFixedSize(150, 50)
        self.label_turn.move(700, 540)
        self.label_turn.setStyleSheet('background-color: #28292E; border-radius: 10px')
        self.label_turn.setText('White')
        self.label_turn.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        self.label_turn.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button_reset = QPushButton('Reset', self)
        self.button_reset.setFixedSize(150, 50)
        self.button_reset.move(700, 600)
        self.button_reset.setStyleSheet('background-color: #28292E; border-radius: 10px')
        self.button_reset.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_reset.setFont(QFont('Arial', 11, QFont.Weight.Bold))

        self.button_next = QPushButton('Next', self)
        self.button_next.setFixedSize(150, 50)
        self.button_next.move(700, 660)
        self.button_next.setStyleSheet('background-color: #28292E; border-radius: 10px')
        self.button_next.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_next.setFont(QFont('Arial', 11, QFont.Weight.Bold))

        self.drag_allowed = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if event.pos().y() < self.title_bar.height():
                self.drag_allowed = True
                self.old_position = event.globalPosition().toPoint()
            else:
                self.drag_allowed = False

    def mouseMoveEvent(self, event):
        if self.drag_allowed and self.old_position:
            delta = event.globalPosition().toPoint() - self.old_position
            self.move(self.pos() + delta)
            self.old_position = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.drag_allowed = False
        self.old_position = None
