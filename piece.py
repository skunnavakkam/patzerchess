class Piece:
    square = int()
    piece = int()

    def __init__(self, Square: int, Piece: int):
        self.square = Square
        self.piece = Piece


'''
board

[■, ■, ■, ■, ■, ■, ■, ■, ■, ■,
 ■, 4, 2, 3, 5, 6, 3, 2, 4, ■,
 ■, 1, 1, 1, 1, 1, 1, 1, 1, ■,
 ■, ., ., ., ., ., ., ., ., ■,
 ■, ., ., ., ., ., ., ., ., ■,
 ■, ., ., ., ., ., ., ., ., ■,
 ■, ., ., ., ., ., ., ., ., ■,
 ■, 7, 7, 7, 7, 7, 7, 7, 7, ■,
 ■,10, 8, 9,11,12, 9, 8,10, ■,
 ■, ■, ■, ■, ■, ■, ■, ■, ■, ■]

the basic board representation, is an array. the array contains 100 elements. 
the ■ on the edge are to make checking for moves off the board, by checking if the
square that you plan to move to is ■. However, the ■ will probably be replaced by 
a different symbol in the code. "." represents empty squares kek

| NUMBER | COLOR | PIECE
| 1      | white | pawn
| 2      | white | knight
| 3      | white | bishop
| 4      | white | rook
| 5      | white | queen
| 6      | white | king
| 7      | black | pawn
  .        .       .
  .        .       .
  .        .       .

this makes it so that you can check piece color. x > 6 is black, x < 7 is white

'''

class Position:

    pieces = list()
    white_ks = bool()
    black_ks = bool()
    white_qs = bool()
    black_qs = bool()
    ep = int()
    hm = int()
    fm = int()
    board = list()
    active_color = bool() # true if w 
    
    # wc = white castle, bc = black castle, ep = enpassant, hm & fm = half and full move clocks
    def __init__(self, board, active_color, castling, ep, hm, fm):

        self.board, self.active_color, self.ep, self.hm, self.fm = board, active_color, ep, hm, fm  

        for e, piece in enumerate(board):
            self.pieces.append(Piece(square=e, piece=piece))

        self.white_ks, self.white_qs = 'K' in castling, 'Q' in castling
        self.black_ks, self.black_qs = 'k' in castling, 'q' in castling
    
    def gen(self):

        for piece in pieces:

            can_move = bool()

            if active_color and piece.piece < 7:

            if piece.piece < 7 and :



