import math
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

        self.setMouseTracking(True)
        self.board.setMouseTracking(True)

        self.files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.pieces: list[Piece] = []
        self.turn = 'White'

        self.selected_square = None

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

        # Test drawing arrow
        test_move_origin = self.square_center("g3")
        test_move_destination = self.square_center("g5")
        self.board.draw_arrow(test_move_origin, test_move_destination)


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            square = self.coordinate_to_square(event.pos())
            if not square: return

            if self.selected_square:
                if self.selected_square == square:
                    self.selected_square = None
                elif self.square_occupied(square):
                    move_uci = self.selected_square + square
                    success = self.execute_move(move_uci)
                    if not success:
                        self.selected_square = square
                else:
                    move_uci = self.selected_square + square
                    success = self.execute_move(move_uci)
                    if not success:
                        self.selected_square = None
            else:
                if self.square_occupied(square):
                    self.selected_square = square

        elif event.button() == Qt.MouseButton.RightButton:
            if self.selected_square:
                self.selected_square = None

    def mouseMoveEvent(self, event):
        square = self.coordinate_to_square(event.pos())
        if not square:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            return
        if self.square_occupied(square):
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def coordinate_to_square(self, coordinate: QPoint):
        file = math.ceil(coordinate.x() / self.square_size)
        rank = math.ceil((self.board.height() - coordinate.y()) / self.square_size)

        if file < 1 or file > 8 or rank < 1 or rank > 8:
            return None
        
        if self.turn == 'White':
            file = self.files[file - 1]
            return file + str(rank)
        else:
            file = self.files[9 - file - 1]
            rank = 9 - rank
            return file + str(rank)

    def square_occupied(self, square: str):
        square = chess.parse_square(square)
        piece = self.board_backend.piece_at(square)
        if piece:
            return True
        else:
            return False

    def execute_move(self, move_uci: str):
        move = chess.Move.from_uci(move_uci)
        if self.board_backend.is_legal(move):
            self.board_backend.push(move)
            self.update_board(self.board_backend.fen())
            self.selected_square = None
            return True
        else:
            return False

    def square_center(self, square: str):
        file = square[0]
        rank = int(square[1])
        file_index = self.files.index(file)
        rank_index = 7 - (rank - 1)

        if self.turn == 'Black':
            file_index = 7 - file_index
            rank_index = rank - 1

        center = QPoint(int((file_index + 0.5) * self.square_size - 1), int((rank_index + 0.5) * self.square_size - 1))
        return center

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
