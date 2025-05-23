import os
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel
from piece_type import PieceType


class Piece(QLabel):
    def __init__(self, type: PieceType, parent=None):
        super(Piece, self).__init__(parent)

        self.type = type
        self.updated = False

        image_name = ''
        if self.type == PieceType.KING_WHITE:
            image_name = 'king_white.png'
        elif self.type == PieceType.KING_BLACK:
            image_name = 'king_black.png'
        elif self.type == PieceType.QUEEN_WHITE:
            image_name = 'queen_white.png'
        elif self.type == PieceType.QUEEN_BLACK:
            image_name = 'queen_black.png'
        elif self.type == PieceType.ROOK_WHITE:
            image_name = 'rook_white.png'
        elif self.type == PieceType.ROOK_BLACK:
            image_name = 'rook_black.png'
        elif self.type == PieceType.BISHOP_WHITE:
            image_name = 'bishop_white.png'
        elif self.type == PieceType.BISHOP_BLACK:
            image_name = 'bishop_black.png'
        elif self.type == PieceType.KNIGHT_WHITE:
            image_name = 'knight_white.png'
        elif self.type == PieceType.KNIGHT_BLACK:
            image_name = 'knight_black.png'
        elif self.type == PieceType.PAWN_WHITE:
            image_name = 'pawn_white.png'
        elif self.type == PieceType.PAWN_BLACK:
            image_name = 'pawn_black.png'

        directory = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(directory, 'images', image_name)

        image = QPixmap(image_path)
        self.setPixmap(image)
        self.setFixedSize(image.size())
        self.setVisible(False)
