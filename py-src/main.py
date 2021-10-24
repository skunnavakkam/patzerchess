
import chess
import chess.svg
import evaluate
import random
from absearch import *
from operator import itemgetter

MATE_VALUE = 524_228 # 2^18

def main():
    board = chess.Board()
    print(board)
    while True:

        print(evaluate.position(board))
        print(board.legal_moves)
        human_move = input("Your move is:")

        if human_move == "kill":
            break

        board.push_san(human_move)

        evl, move = alpha_beta(-MATE_VALUE, MATE_VALUE, 3, board)

        print(f"{(move)} was my move")
        board.push(move)
        print(board)




if __name__ == "__main__":
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()