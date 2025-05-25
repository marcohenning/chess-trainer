import io
import random
import zstandard
import chess.pgn


games_database = 'C:/Users/MH/Desktop/games.zst'

with open(games_database, 'rb') as compressed:
    decompressor = zstandard.ZstdDecompressor()
    with decompressor.stream_reader(compressed) as reader:
        text_stream = io.TextIOWrapper(reader, encoding='utf-8')
        count = 0

        while count < 1:
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

            print(position_fen)
            print([previous_move_uci, previous_move_algebraic])
            print(next_move_uci)
            print(str(game))
