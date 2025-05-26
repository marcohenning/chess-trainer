import os
import io
import random
import zstandard
import chess.pgn


games_database = 'D:/Files/lichess_2025_april.zst'

with open(games_database, 'rb') as compressed:
    decompressor = zstandard.ZstdDecompressor()
    with decompressor.stream_reader(compressed) as reader:
        text_stream = io.TextIOWrapper(reader, encoding='utf-8')
        count = 0

        while count < 1000000:
            game = chess.pgn.read_game(text_stream)
            if game is None:
                break

            moves = list(game.mainline_moves())
            move_amount = len(moves)

            if move_amount < 5:
                continue
        
            count += 1

            index = random.randint(3, move_amount - 2)
            previous_move = moves[index - 1]
            next_move = moves[index]

            board = game.board()
            for move in moves[:index]:
                board.push(move)

            position_fen = board.fen()
            next_move_uci = next_move.uci()

            board_before = game.board()
            for move in moves[:index - 1]:
                board_before.push(move)

            previous_move_uci = previous_move.uci()
            previous_move_algebraic = board_before.san(previous_move)

            file_name = '1.txt'

            if count > 100000:
                file_name = '2.txt'
            if count > 200000:
                file_name = '3.txt'
            if count > 300000:
                file_name = '4.txt'
            if count > 400000:
                file_name = '5.txt'
            if count > 500000:
                file_name = '6.txt'
            if count > 600000:
                file_name = '7.txt'
            if count > 700000:
                file_name = '8.txt'
            if count > 800000:
                file_name = '9.txt'
            if count > 900000:
                file_name = '10.txt'

            directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(directory, 'positions', file_name)

            with open(file_path, 'a') as file:
                file.write('{}|{}|{}|{}\n'.format(position_fen, previous_move_uci, previous_move_algebraic, next_move_uci))
