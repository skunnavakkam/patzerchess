
import chess
import eval
import random
from absearch import search, qs_search
from operator import itemgetter


def main():
    board = chess.Board(
        fen="r1bqkbnr/ppp2ppp/2np4/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 4")

    print(qs_search(board, 0))

    print(board)


if __name__ == "__main__":
    main()
