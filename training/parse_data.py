
import chess
import random

def find_positions(moves_list, result) -> tuple:
    
    positions = []

    board = chess.Board()

    for num_moves, move in enumerate(moves_list):

        if move == "0-1" or move == "1-0" or move == "1/2-1/2":
            continue

        board.push_san(move)

        b = str(board)

        w_material = (
            1 * b.count('P') +
            3 * b.count('N') +
            3 * b.count('B') +
            5 * b.count('R') + 
            9 * b.count('Q')
        )

        b_material = (
            1 * b.count('p') + 
            3 * b.count('n') + 
            3 * b.count('b') + 
            5 * b.count('r') + 
            9 * b.count('q')
        )

        if ((w_material < 27 or b_material < 27) or num_moves > 14):
            positions.append((board.fen(), result))

    if len(positions) != 0:
        return random.choice(positions)
    else:
        return None