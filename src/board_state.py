

class BoardState():
    def __init__(self, fen: str, move_uci: str, move_algebraic: str):
        self.fen = fen
        self.move_uci = move_uci
        self.move_algebraic = move_algebraic

    def get_fen(self):
        return self.fen
    
    def get_move_uci(self):
        return self.move_uci
    
    def get_move_algebraic(self):
        return self.move_algebraic
