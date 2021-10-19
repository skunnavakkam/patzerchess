
import chess
import eval
import random
from absearch import *
from operator import itemgetter

MATE_VALUE = -30_000


def main():
    board = chess.Board(
        fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    moves = get_moves(board, 1)

    for move in moves:
        print(move)


if __name__ == "__main__":
    main()
