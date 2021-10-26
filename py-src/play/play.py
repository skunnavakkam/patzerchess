
import chess
import chess.svg
import evaluate
import random
from absearch import ABSearcher
from operator import itemgetter
import time

MATE_VALUE = 524_228 # 2^18

def main():

    board = chess.Board()
    searcher = ABSearcher()


    while True:

        print(board, "\n\n")

        # gets the human move
        move_bad = True
        while move_bad:
            human_move = input("Input your move: ")
            try:
                move = board.parse_san(human_move)
                board.push(move)
                move_bad = False
            except Exception as e:
                print(e)
                print("Please input a legal move in SAN format")
        
        print(board, "\n\n")

        t = time.time()
        for evl, move in searcher.search(board):
            if time.time() - t > 1:
                print(f"My move was {board.san(move)}")
                board.push(move)
                break        




if __name__ == "__main__":
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()