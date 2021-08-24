class piece:
    square = int()
    piece = int()

    def __init__(self, Square: int, Piece: int):
        self.square = Square
        self.piece = Piece


class board:
    pieces = list()
    wc = int()
    bc = int()
    

    def __init__(self)