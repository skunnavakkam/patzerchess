from board import Position

def main():
    board = Position()

    print(as_board(board.WQ))

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