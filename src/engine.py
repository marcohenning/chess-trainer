import os
import time
import chess
import chess.engine
from PyQt6.QtCore import QThread, pyqtSignal


class Engine(QThread):

    analysis_finished = pyqtSignal()
    analysis_updated = pyqtSignal(str, list)

    def __init__(self, fen: str):
        super().__init__()

        self.board = chess.Board(fen)
        self.move_amount = min(5, self.board.legal_moves.count())

        self.directory = os.path.dirname(os.path.abspath(__file__))
        """file_name = ''
        engine_path = os.path.join(self.directory, 'stockfish', file_name)"""
        engine_path = 'C:/Users/MH/Desktop/stockfish/stockfish-windows-x86-64-avx2.exe' #temp
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.running = True

    def run(self):
        try:
            start_time = time.time()
            with self.engine.analysis(self.board, multipv=self.move_amount) as analysis:
                seen = {}

                for information in analysis:
                    if not self.running or time.time() - start_time > 5.0:
                        self.analysis_finished.emit()
                        break
                    if 'score' in information and 'pv' in information:
                        multipv = information.get('multipv', 1)
                        if multipv >= 1 and multipv <= self.move_amount:
                            move = self.board.san(information['pv'][0])
                            evaluation = information['score'].white()

                            # TODO: Format eval strings correctly
                            if evaluation.is_mate():
                                evaluation_string = 'M{}'.format(evaluation.mate())
                            else:
                                evaluation_string = '{}'.format(evaluation.score() / 100.0)
                            
                            seen[multipv] = (move, evaluation_string)

                        if len(seen) == self.move_amount:
                            moves = []
                            for i in range(self.move_amount):
                                move, evaluation = seen[i + 1]
                                moves.append([move, evaluation])

                            self.analysis_updated.emit(moves[0][1], moves)
                            seen.clear()

        except Exception as exception:
            pass
        finally:
            self.engine.quit()

    def stop(self):
        self.running = False
