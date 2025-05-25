import os
import math
import chess
import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtWidgets import QWidget, QPushButton
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

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.button_queen = QPushButton('Queen', self)
        self.button_queen.setFixedSize(75, 24)
        self.button_queen.setVisible(False)
        self.button_queen.pressed.connect(self.handle_button_queen)
        self.button_queen.setFont(QFont('Arial', 9))

        self.button_rook = QPushButton('Rook', self)
        self.button_rook.setFixedSize(75, 24)
        self.button_rook.setVisible(False)
        self.button_rook.pressed.connect(self.handle_button_rook)
        self.button_rook.setFont(QFont('Arial', 9))

        self.button_bishop = QPushButton('Bishop', self)
        self.button_bishop.setFixedSize(75, 24)
        self.button_bishop.setVisible(False)
        self.button_bishop.pressed.connect(self.handle_button_bishop)
        self.button_bishop.setFont(QFont('Arial', 9))

        self.button_knight = QPushButton('Knight', self)
        self.button_knight.setFixedSize(75, 24)
        self.button_knight.setVisible(False)
        self.button_knight.pressed.connect(self.handle_button_knight)
        self.button_knight.setFont(QFont('Arial', 9))

        self.setMouseTracking(True)
        self.board.setMouseTracking(True)

        self.setStyleSheet('QPushButton {background-color: #28292E; border: 1px solid #484C54;} QPushButton:hover {background-color: #35363D;}')

        self.directory = os.path.dirname(os.path.abspath(__file__))

        pygame.mixer.init()

        self.files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.pieces: list[Piece] = []
        self.turn = 'White'
        self.move_uci = None

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

        fen = '1nbqkbnr/P1pppppp/1r6/1p6/P7/8/2PPPPPP/RNBQKBNR w KQk - 1 6'
        self.board_backend = chess.Board(fen)
        self.update_board(fen)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:

            if self.button_queen.isVisible():
                self.selected_square = None
                self.move_uci = None
                self.hide_promotion_prompt()
                return

            square = self.coordinate_to_square(event.pos())
            if not square: return

            if self.selected_square:
                if self.selected_square == square:
                    self.selected_square = None
                elif self.square_occupied(square):
                    move_uci = self.selected_square + square
                    
                    can_promote = self.can_promote(move_uci)
                    if can_promote: return

                    success = self.execute_move(move_uci)
                    if not success:
                        self.selected_square = square
                else:
                    move_uci = self.selected_square + square

                    can_promote = self.can_promote(move_uci)
                    if can_promote: return

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
        move_algebraic = self.board_backend.san(move)

        if self.board_backend.is_legal(move):
            self.board_backend.push(move)
            self.update_board(self.board_backend.fen())

            # Draw arrow
            origin = self.square_center(move_uci[:2])
            destination = self.square_center(move_uci[2:])
            self.board.draw_arrow(origin, destination)

            sound = 'place.wav'
            if '+' in move_algebraic or '#' in move_algebraic:
                sound = 'check.wav'
            elif 'x' in move_algebraic:
                sound = 'capture.wav'
            elif '-' in move_algebraic:
                sound = 'castling.wav'

            pygame.mixer.music.stop()
            sound_path = os.path.join(self.directory, 'sounds', sound)
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()

            self.selected_square = None
            self.move_uci = None
            return True
        else:
            return False

    def can_promote(self, move_uci: str):
        move = chess.Move.from_uci(move_uci + 'q')
        if self.board_backend.is_legal(move):
            self.move_uci = move_uci
            self.show_promotion_prompt()
            return True
        else:
            return False
        
    def show_promotion_prompt(self):
        self.button_queen.setVisible(True)
        self.button_rook.setVisible(True)
        self.button_bishop.setVisible(True)
        self.button_knight.setVisible(True)

        global_cursor_position = QCursor.pos()
        local_cursor_position = self.mapFromGlobal(global_cursor_position)

        promotion_prompt_bottom_right = QPoint()
        promotion_prompt_height = self.button_queen.height() * 4 - 3
        promotion_prompt_bottom_right.setX(local_cursor_position.x() + self.button_queen.width())
        promotion_prompt_bottom_right.setY(local_cursor_position.y() + promotion_prompt_height)

        promotion_prompt_position = QPoint(local_cursor_position)

        if promotion_prompt_bottom_right.x() >= self.board.width():
            promotion_prompt_position.setX(local_cursor_position.x() - (self.button_queen.width() - 1))
        if promotion_prompt_bottom_right.y() >= self.board.height():
            promotion_prompt_position.setY(local_cursor_position.y() - (promotion_prompt_height - 1))

        self.button_queen.move(promotion_prompt_position)
        self.button_rook.move(self.button_queen.pos().x(), self.button_queen.pos().y() + self.button_queen.height() - 1)
        self.button_bishop.move(self.button_rook.pos().x(), self.button_rook.pos().y() + self.button_rook.height() - 1)
        self.button_knight.move(self.button_bishop.pos().x(), self.button_bishop.pos().y() + self.button_bishop.height() - 1)

    def hide_promotion_prompt(self):
        self.button_queen.setVisible(False)
        self.button_rook.setVisible(False)
        self.button_bishop.setVisible(False)
        self.button_knight.setVisible(False)

    def execute_promotion(self, piece: str):
        self.hide_promotion_prompt()
        if self.move_uci:
            self.execute_move(self.move_uci + piece)

    def handle_button_queen(self):
        self.execute_promotion('q')

    def handle_button_rook(self):
        self.execute_promotion('r')

    def handle_button_bishop(self):
        self.execute_promotion('b')

    def handle_button_knight(self):
        self.execute_promotion('n')

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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            print('Left')
        elif event.key() == Qt.Key.Key_Right:
            print('Right')
