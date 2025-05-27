from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel
from PyQt6.QtGui import QFont
from board import Board
from position_loader import PositionLoader


class Window(QWidget):
    def __init__(self):
        super().__init__(parent=None)

        self.setFixedSize(880, 740)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet('color: #FFF;')

        screen = self.screen().availableGeometry()
        size = self.geometry()
        x = screen.center().x() - size.width() // 2
        y = screen.center().y() - size.height() // 2
        self.move(x + 1, y + 1)

        self.position = []

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
        self.button_close.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.button_minimize = QPushButton(self)
        self.button_minimize.setFixedSize(14, 14)
        self.button_minimize.move(829, 13)
        self.button_minimize.clicked.connect(self.showMinimized)
        self.button_minimize.setStyleSheet('background-color: #EBC631; border-radius: 7px;')
        self.button_minimize.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_minimize.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.board = Board(self)
        self.board.move(30, 70)
        self.board.live_engine_updated.connect(self.update_live_engine_labels)
        self.board.loss_engine_updated.connect(self.update_loss_label)

        self.position_loader = PositionLoader()

        self.label_result = QLabel(self)
        self.label_result.setFixedSize(150, 70)
        self.label_result.move(700, 70)
        self.label_result.setStyleSheet('background-color: #28292E; border-radius: 10px')
        self.label_result.setFont(QFont('Arial', 15, QFont.Weight.Bold))
        self.label_result.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.engine_evaluation = QLabel(self)
        self.engine_evaluation.setFixedSize(150, 50)
        self.engine_evaluation.move(700, 145)
        self.engine_evaluation.setStyleSheet('background-color: #28292E; border-radius: 10px')
        self.engine_evaluation.setFont(QFont('Arial', 15, QFont.Weight.Bold))
        self.engine_evaluation.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.engine_move_1 = QLabel(self)
        self.engine_move_1.setFixedSize(150, 50)
        self.engine_move_1.move(700, self.engine_evaluation.y() + self.engine_evaluation.height() + 5)
        self.engine_move_1.setStyleSheet('background-color: #28292E; border-radius: 10px')
        self.engine_move_1.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        self.engine_move_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.engine_move_2 = QLabel(self)
        self.engine_move_2.setFixedSize(150, 50)
        self.engine_move_2.move(700, self.engine_move_1.y() + self.engine_move_1.height() + 5)
        self.engine_move_2.setStyleSheet('background-color: #28292E; border-radius: 10px')
        self.engine_move_2.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        self.engine_move_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.engine_move_3 = QLabel(self)
        self.engine_move_3.setFixedSize(150, 50)
        self.engine_move_3.move(700, self.engine_move_2.y() + self.engine_move_2.height() + 5)
        self.engine_move_3.setStyleSheet('background-color: #28292E; border-radius: 10px')
        self.engine_move_3.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        self.engine_move_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.engine_move_4 = QLabel(self)
        self.engine_move_4.setFixedSize(150, 50)
        self.engine_move_4.move(700, self.engine_move_3.y() + self.engine_move_3.height() + 5)
        self.engine_move_4.setStyleSheet('background-color: #28292E; border-radius: 10px')
        self.engine_move_4.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        self.engine_move_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.engine_move_5 = QLabel(self)
        self.engine_move_5.setFixedSize(150, 50)
        self.engine_move_5.move(700, self.engine_move_4.y() + self.engine_move_4.height() + 5)
        self.engine_move_5.setStyleSheet('background-color: #28292E; border-radius: 10px')
        self.engine_move_5.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        self.engine_move_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.engine_move_labels = []
        self.engine_move_labels.append(self.engine_move_1)
        self.engine_move_labels.append(self.engine_move_2)
        self.engine_move_labels.append(self.engine_move_3)
        self.engine_move_labels.append(self.engine_move_4)
        self.engine_move_labels.append(self.engine_move_5)

        self.button_reset = QPushButton('Reset', self)
        self.button_reset.setFixedSize(150, 50)
        self.button_reset.move(700, 605)
        self.button_reset.setStyleSheet('QPushButton {background-color: #28292E; border-radius: 10px;} QPushButton:hover {background-color: #2C2D33;} QPushButton:disabled {background-color: #2C2D33;}')
        self.button_reset.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_reset.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        self.button_reset.setDisabled(True)
        self.button_reset.clicked.connect(self.reset_position)
        self.button_reset.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.button_start_next = QPushButton('Start', self)
        self.button_start_next.setFixedSize(150, 50)
        self.button_start_next.move(700, 660)
        self.button_start_next.setStyleSheet('QPushButton {background-color: #28292E; border-radius: 10px;} QPushButton:hover {background-color: #2C2D33;} QPushButton:disabled {background-color: #2C2D33;}')
        self.button_start_next.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button_start_next.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        self.button_start_next.clicked.connect(self.load_position)
        self.button_start_next.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.board.attempt_made.connect(self.enable_button_start_next)

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

    def load_position(self):
        self.board.stop_engines()

        position_fen, previous_move_uci, previous_move_algebraic, next_move_uci = self.position_loader.get_position()
        self.position = [position_fen, previous_move_uci, previous_move_algebraic, next_move_uci]

        self.board.load_position(position_fen, previous_move_uci, previous_move_algebraic, next_move_uci)
        self.button_start_next.setEnabled(False)
        
        if self.button_start_next.text() == 'Start':
            self.button_start_next.setText('Next')
            self.button_reset.setEnabled(True)

        for label in self.engine_move_labels:
            label.setText('')
        
        self.engine_evaluation.setText('')
        self.label_result.setText('')

    def enable_button_start_next(self):
        self.button_start_next.setEnabled(True)

    def update_live_engine_labels(self, evaluation, moves):
        self.engine_evaluation.setText(evaluation)

        for label in self.engine_move_labels:
            label.setText('')

        for i in range(len(moves)):
            self.engine_move_labels[i].setText('{} ({})'.format(moves[i][0], moves[i][1]))

    def update_loss_label(self, loss):
        self.label_result.setText(loss)

    def closeEvent(self, event):
        self.board.stop_engines()
        event.accept()

    def reset_position(self):
        self.board.stop_engines()
        self.board.load_position(self.position[0], self.position[1], self.position[2], self.position[3])
        self.button_start_next.setEnabled(False)

        for label in self.engine_move_labels:
            label.setText('')
        
        self.engine_evaluation.setText('')
        self.label_result.setText('')
