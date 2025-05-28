import os
import math
import chess
import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtWidgets import QWidget, QPushButton
from piece import Piece
from board_image import BoardImage
from board_state import BoardState
from piece_type import PieceType
from engine import Engine


class Board(QWidget):

    attempt_made = pyqtSignal()
    live_engine_updated = pyqtSignal(str, list)
    loss_engine_updated = pyqtSignal(str)
    game_over = pyqtSignal(str)

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
        self.board_states: list[Board] = []
        self.board_state_index = 1
        self.turn = 'White'
        self.move_uci = None
        self.selected_square = None
        self.input_disabled = True
        self.attempt = False
        self.attempt_move = None
        self.initial_evaluation = None
        self.initial_evaluation_move = None
        self.live_engine = None
        self.initial_engine = None
        self.loss_engine = None

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

        self.board_backend = chess.Board()
        self.update_board(self.board_backend.fen())

    def mousePressEvent(self, event):
        if self.input_disabled: return

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

            if not self.attempt:
                self.attempt = True
                self.attempt_move = move_algebraic

                self.loss_engine = Engine(self.board_backend.fen())
                self.loss_engine.analysis_updated.connect(self.handle_loss_engine_updated)
                self.loss_engine.start()

                self.attempt_made.emit()

            if len(self.board_states) > self.board_state_index + 1:
                if self.board_backend.fen() == self.board_states[self.board_state_index + 1].get_fen():
                    self.board_state_index += 1
                else:
                    self.board_states = self.board_states[:self.board_state_index + 1]
                    self.board_states.append(BoardState(self.board_backend.fen(), move_uci, move_algebraic))
                    self.board_state_index += 1
            else:
                self.board_states.append(BoardState(self.board_backend.fen(), move_uci, move_algebraic))
                self.board_state_index += 1
            
            self.set_input_disabled(False)
            self.load_board_state()
            return True
        else:
            return False

    def load_board_state(self):
        fen = self.board_states[self.board_state_index].get_fen()
        move_uci = self.board_states[self.board_state_index].get_move_uci()
        move_algebraic = self.board_states[self.board_state_index].get_move_algebraic()

        self.board_backend.set_fen(fen)
        self.update_board(fen)

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

        if self.attempt:
            if self.live_engine:
                self.live_engine.stop()
                try:
                    self.live_engine.analysis_updated.disconnect(self.handle_live_engine_updated)
                except:
                    pass
            self.live_engine = Engine(fen)
            self.live_engine.analysis_updated.connect(self.handle_live_engine_updated)
            self.live_engine.start()

            if self.board_backend.is_checkmate():
                loser = self.board_backend.turn
                if loser == chess.WHITE:
                    message = '0 - 1'
                else:
                    message = '1 - 0'
                self.game_over.emit(message)
                
            elif self.board_backend.is_stalemate() or self.board_backend.is_insufficient_material():
                self.game_over.emit('1/2 - 1/2')

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
        if self.button_queen.isVisible(): return

        if event.key() == Qt.Key.Key_Left:
            if self.board_state_index >= 1:
                self.board_state_index -= 1
                self.load_board_state()
                if self.board_state_index == 0:
                    self.set_input_disabled(True)
        elif event.key() == Qt.Key.Key_Right:
            if self.board_state_index <= len(self.board_states) - 2:
                self.board_state_index += 1
                self.load_board_state()
                self.set_input_disabled(False)

    def set_input_disabled(self, disabled: bool):
        self.input_disabled = disabled

    def load_position(self, position_fen, previous_move_uci, previous_move_algebraic, next_move_uci):
        self.board_states.clear()
        self.board_state_index = 1

        self.board_states.append(BoardState(position_fen, previous_move_uci, previous_move_algebraic))

        self.board_backend.set_fen(position_fen)
        next_move = chess.Move.from_uci(next_move_uci)
        next_move_algebraic = self.board_backend.san(next_move)
        self.board_backend.push(next_move)

        self.board_states.append(BoardState(self.board_backend.fen(), next_move_uci, next_move_algebraic))

        if self.board_backend.fen().split(' ')[1] == 'w':
            self.turn = 'White'
        else:
            self.turn = 'Black'

        self.hide_promotion_prompt()
        self.set_input_disabled(False)

        self.move_uci = None
        self.selected_square = None
        self.attempt = False
        self.attempt_move = None
        self.initial_evaluation = None
        self.initial_evaluation_move = None

        self.load_board_state()

        self.set_input_disabled(True)
        self.initial_engine = Engine(self.board_backend.fen())
        self.initial_engine.analysis_updated.connect(self.handle_initial_engine_updated)
        self.initial_engine.analysis_finished.connect(self.handle_initial_engine_finished)
        self.initial_engine.start()

    def handle_live_engine_updated(self, evaluation, moves):
        self.live_engine_updated.emit(evaluation, moves)

    def handle_initial_engine_updated(self, evaluation, moves):
        self.initial_evaluation = evaluation
        self.initial_evaluation_move = moves[0][0]

    def handle_initial_engine_finished(self):
        self.set_input_disabled(False)

    def handle_loss_engine_updated(self, evaluation, moves):
        loss = 'N/A'

        favorable_sign = '+'
        if self.turn == 'Black':
            favorable_sign = '-'

        mate_number_initial = ''
        if 'M' in self.initial_evaluation:
            mate_number_initial = int(self.initial_evaluation[2:])
        mate_number_now = ''
        if 'M' in evaluation:
            mate_number_now = int(evaluation[2:])

        if not 'M' in self.initial_evaluation and not 'M' in evaluation:
            if self.initial_evaluation_move == self.attempt_move:
                loss = '0.00'
            else:
                loss = '{:.2f}'.format(abs(float(self.initial_evaluation) - float(evaluation)))

        elif not 'M' in self.initial_evaluation and 'M' in evaluation:
            if evaluation[0] == favorable_sign:
                loss = '0.00'
            else:
                loss = '#'

        elif 'M' in self.initial_evaluation and self.initial_evaluation[0] == favorable_sign:
            if not 'M' in evaluation:
                loss = self.initial_evaluation
            elif 'M' in evaluation and evaluation[0] != favorable_sign:
                loss = '#'
            elif mate_number_now >= mate_number_initial:
                loss = self.initial_evaluation
            elif mate_number_now < mate_number_initial:
                loss = '0.00'

        elif 'M' in self.initial_evaluation and self.initial_evaluation[0] != favorable_sign:
            if not 'M' in evaluation or ('M' in evaluation and evaluation[0] == favorable_sign) or mate_number_now >= mate_number_initial:
                loss = '0.00'
            elif mate_number_now == mate_number_initial:
                loss = '0.00'
            elif mate_number_now < mate_number_initial:
                loss = self.initial_evaluation
        
        self.loss_engine_updated.emit(loss)

    def stop_engines(self):
        if self.initial_engine:
            self.initial_engine.stop()
            self.initial_engine.quit()
            self.initial_engine.wait()
        
        if self.loss_engine:
            self.loss_engine.stop()
            self.loss_engine.quit()
            self.loss_engine.wait()

        if self.live_engine:
            self.live_engine.stop()
            self.live_engine.quit()
            self.live_engine.wait()

    def disconnect_engines(self):
        if self.initial_engine:
            self.initial_engine.stop()
            try:
                self.initial_engine.analysis_updated.disconnect(self.handle_initial_engine_updated)
            except:
                pass
            try:
                self.initial_engine.analysis_finished.disconnect(self.handle_initial_engine_finished)
            except:
                pass

        if self.loss_engine:
            self.loss_engine.stop()
            try:
                self.loss_engine.analysis_updated.disconnect(self.handle_loss_engine_updated)
            except:
                pass

        if self.live_engine:
            self.live_engine.stop()
            try:
                self.live_engine.analysis_updated.disconnect(self.handle_live_engine_updated)
            except:
                pass
