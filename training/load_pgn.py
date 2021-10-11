
'''
Possible game ends are 

1-0
0-1
1/2-1/2

so to detect the end of the game, you just have to detect one of these
'''

from parse_data import *
import re

with open("lichess_db_standard_rated_2020-03.pgn/lichess_db_standard_rated_2020-03.pgn") as file:

    to_print = ""

    for line in file:
        to_print += line # o^2 but the variable won't get too large so it should be fine

        if ("1/2-1/2" in line or "1-0" in line or "0-1" in line) and "Result" not in line:
            # act on the pgn that has been stored
            try:
                rating_white = int(re.findall('WhiteElo\s"([0-9]+)"', to_print)[0])
                rating_black = int(re.findall('BlackElo\s"([0-9]+)"', to_print)[0])

                if rating_white > 2000 and rating_black > 2000 and "Time forfeit" not in to_print:

                    moves_list = re.findall('\s([a-zA-Z0-9=-]+)[+!?#]*\s', line)
                    result_str = re.findall('\s(\S*[0-9]-[0-9]\S*)', line )[0]

                    result_dict = {"1-0":1, "0-1": 0, "1/2-1/2": 0.5}
                    result = result_dict[result_str]
                
                    try:
                        position = find_positions(moves_list, result)
                    except:
                        print("An error, we skipped it")


                    with open('positions.txt', 'a') as f:
                        f.write("|".join(str(p) for p in position) + "\n")
            except:
                print("An error, we skipped it")

            to_print = ""