import chess
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QWidget
from piece import Piece
from board_image import BoardImage
from piece_type import PieceType


class Board(QWidget):
    def __init__(self, parent=None):
        super(Board, self).__init__(parent)

        self.board = BoardImage(self)
        self.setFixedSize(self.board.size())
        self.square_size = self.board.width() // 8
        self.board_rectangle = self.board.rect()

        self.files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.pieces: list[Piece] = []
        self.turn = 'White'

        self.letter_to_piece_type = {
            "K": PieceType.KING_WHITE,
            "k": PieceType.KING_BLACK,
            "Q": PieceType.QUEEN_WHITE,
            "q": PieceType.QUEEN_BLACK,
            "R": PieceType.ROOK_WHITE,
            "r": PieceType.ROOK_BLACK,
            "B": PieceType.BISHOP_WHITE,
            "b": PieceType.BISHOP_BLACK,
            "N": PieceType.KNIGHT_WHITE,
            "n": PieceType.KNIGHT_BLACK,
            "P": PieceType.PAWN_WHITE,
            "p": PieceType.PAWN_BLACK
        }

        self.pieces.append(Piece(PieceType.KING_WHITE, self.board))
        self.pieces.append(Piece(PieceType.KING_BLACK, self.board))

        for i in range(9):
            self.pieces.append(Piece(PieceType.QUEEN_WHITE, self.board))
            self.pieces.append(Piece(PieceType.QUEEN_BLACK, self.board))

        for i in range(10):
            self.pieces.append(Piece(PieceType.ROOK_WHITE, self.board))
            self.pieces.append(Piece(PieceType.ROOK_BLACK, self.board))
            self.pieces.append(Piece(PieceType.BISHOP_WHITE, self.board))
            self.pieces.append(Piece(PieceType.BISHOP_BLACK, self.board))
            self.pieces.append(Piece(PieceType.KNIGHT_WHITE, self.board))
            self.pieces.append(Piece(PieceType.KNIGHT_BLACK, self.board))

        for i in range(8):
            self.pieces.append(Piece(PieceType.PAWN_WHITE, self.board))
            self.pieces.append(Piece(PieceType.PAWN_BLACK, self.board))

        fen = 'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3'
        self.board_backend = chess.Board(fen)
        self.update_board(fen)

    def update_board(self, fen: str):
        fen_shortened = fen.split(' ')[0]
        ranks = fen_shortened.split('/')

        piece_position = QPoint()
        if self.turn == 'White':
            piece_position = QPoint(self.board_rectangle.topLeft().x(), self.board_rectangle.topLeft().y() - self.square_size)
        else:
            piece_position = QPoint(self.board_rectangle.bottomRight().x() - self.square_size, self.board_rectangle.bottomRight().y())
        
        for piece in self.pieces:
            piece.setVisible(False)
            piece.updated = False

        for rank in ranks:
            if self.turn == 'White':
                piece_position.setX(self.board_rectangle.topLeft().x())
                piece_position.setY(piece_position.y() + self.square_size)
            else:
                piece_position.setX(self.board_rectangle.bottomRight().x() - self.square_size)
                piece_position.setY(piece_position.y() - self.square_size)

            for character in rank:
                if character.isdigit():
                    for i in range(int(character)):
                        if self.turn == 'White':
                            piece_position.setX(piece_position.x() + self.square_size)
                        else:
                            piece_position.setX(piece_position.x() - self.square_size)
                else:
                    piece_type = self.letter_to_piece_type[character]
                    for piece in self.pieces:
                        if piece.type == piece_type and not piece.updated:
                            piece.move(piece_position)
                            piece.updated = True
                            piece.setVisible(True)

                            if self.turn == 'White':
                                piece_position.setX(piece_position.x() + self.square_size)
                            else:
                                piece_position.setX(piece_position.x() - self.square_size)
                            break
