def main():

    from board import Position
    from time import time

    board = Position('K6k/8/8/8/8/8/8/8 w - - 0 1')



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