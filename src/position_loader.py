import os
import random


class PositionLoader():
    def __init__(self):
        self.directory = os.path.dirname(os.path.abspath(__file__))

    def get_position(self):
        file_name = '{}.txt'.format(random.randint(1, 10))
        file_path = os.path.join(self.directory, 'positions', file_name)
        
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file]

            position = lines[random.randint(0, len(lines) - 1)]
            position_elements = position.split('|')
            
            position_fen = position_elements[0]
            previous_move_uci = position_elements[1]
            previous_move_algebraic = position_elements[2]
            next_move_uci = position_elements[3]

            return position_fen, previous_move_uci, previous_move_algebraic, next_move_uci
