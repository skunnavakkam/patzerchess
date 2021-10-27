
'''
Possible game ends are 

1-0
0-1
1/2-1/2

so to detect the end of the game, you just have to detect one of these

run this "C:\Program Files\pypy3.7-v7.3.5-win64\pypy3.exe" load_pgn.py
'''

import chess
import chess.pgn
import io
import random

def parse_pgn(file):

    with open(file) as f:

        # write heads for train, test, and cross-validation sets
        # have to do something like this bc too much data to store in memory
        f_train = open("training-data/train.txt", "a")
        f_test = open("training-data/test.txt", "a")
        f_cv = open("training-data/cv.txt", "a")

        to_print = ""
        for line in f:
            to_print += line
            if ("0-1" in line or "1-0" in line or "1/2-1/2" in line) and "Result" not in line:
                
                pgn = io.StringIO(to_print)
                game = chess.pgn.read_game(pgn)
                to_print = ""

                positions = list(game.mainline())
                choice = random.randrange(len(positions)-1)

                position = positions[choice].board().fen()
                next_move = str(positions[choice + 1].move)

                to_write = "|".join((position, next_move, game.headers["Result"])) + "\n"

                writer = random.randint(1,11) # generating between 1 and 11 inclusive

                if writer <= 6:
                    f_train.write(to_write)
                elif writer <= 8:
                    f_cv.write(to_write)
                else:
                    f_test.write(to_write)
        
        f_train.close()
        f_test.close()
        f_cv.close()
                
                







def main():

    parse_pgn("raw-data/KingBase2019-A00-A39.pgn")


if __name__ == '__main__':
    main()
