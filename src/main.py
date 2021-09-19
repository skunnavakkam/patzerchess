def main():

    from board import Position
    from timeit import timeit

    board = Position('1k6/8/8/8/R7/8/8/K7 w - - 0 1')
    
    time = timeit(lambda: board._gen_out_of_check(), number = 10000)/10000

    print(time)


def as_board(bitboard):
    return_string = ""
    bb = bin(bitboard)[2:][::-1]
    for square, bit in enumerate( (bb + ((64 - len(bb)) * "0")) ):
        return_string += bit
        return_string += " "
        if square % 8 == 7:
            return_string += "\n"
    return return_string

if __name__ == "__main__":
    main()