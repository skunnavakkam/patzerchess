
'''
Possible game ends are 

1-0
0-1
1/2-1/2

so to detect the end of the game, you just have to detect one of these

run this "C:\Program Files\pypy3.7-v7.3.5-win64\pypy3.exe" load_pgn.py
'''

from parse_data import *
import re
import time


def parse_stuff(line, to_print):
    try:
        rating_white = int(re.findall(
            'WhiteElo\s"([0-9]+)"', to_print)[0])
        rating_black = int(re.findall(
            'BlackElo\s"([0-9]+)"', to_print)[0])

        moves_list = re.findall(
            '\s([a-zA-Z0-9=-]+)[+!?#]*\s', line)
        result_str = re.findall('\s(\S*[0-9]-[0-9]\S*)', line)[0]

        result_dict = {"1-0": 1, "0-1": 0, "1/2-1/2": 0.5}
        result = result_dict[result_str]

        position = find_positions(moves_list, result)

        if position is not None:
            with open('positions.txt', 'a') as f:
                f.write("|".join(str(p) for p in position) + "\n")
    except:
        pass


def load_pgn():
    with open("raw-data/KingBase2019-A00-A39.pgn") as file:

        to_print = ""
        for line in file:
            to_print += line  # o^2 but the variable won't get too large so it should be fine

            if ("1/2-1/2" in line or "1-0" in line or "0-1" in line) and "Result" not in line:
                # act on the pgn that has been stored

                # tasks.append(
                #     Process(target=parse_stuff, args=(line, to_print)))

                parse_stuff(line, to_print)

                to_print = ""


def main():

    load_pgn()


if __name__ == '__main__':
    main()
