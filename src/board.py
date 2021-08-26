
'''
board

[14,14,14,14,14,14,14,14,14,14,
 14, 4, 2, 3, 5, 6, 3, 2, 4,14,
 14, 1, 1, 1, 1, 1, 1, 1, 1,14,
 14, 0, 0, 0, 0, 0, 0, 0, 0,14,
 14, 0, 0, 0, 0, 0, 0, 0, 0,14,
 14, 0, 0, 0, 0, 0, 0, 0, 0,14,
 14, 0, 0, 0, 0, 0, 0, 0, 0,14,
 14, 7, 7, 7, 7, 7, 7, 7, 7,14,
 14,10, 8, 9,11,12, 9, 8,10,14,
 14,14,14,14,14,14,14,14,14,14]

the basic board representation, is an array. the array contains 100 elements. 
the "14" on the edge are to make checking for moves off the board, by checking if the
square that you plan to move to is "14". However, the "14" will probably be replaced by 
a different symbol in the code. "13" represents empty squares kek

| NUMBER | COLOR | PIECE
| 1      | white | pawn
| 2      | white | knight
| 3      | white | bishop
| 4      | white | rook
| 5      | white | queen
| 6      | white | king
| 7      | black | pawn
| .      | .     | .
| .      | .     | .
| .      | .     | .
| 0      | none  | empty
| 13     | none  | out of board
this makes it so that you can check piece color. x > 6 is black, x < 7 is white

'''

N, S, W, E = 10, -10, 1, -1

# directions for sliding pieces
directions = {
    3: (N+W, S+W, N+E, S+E), # bishop
    4: (N, S, W, E),
    5: (N, S, W, E, N+W, S+W, N+E, S+E)
}

class Piece:
    square = int()
    piece = int()

    def __init__(self, Square: int, Piece: int):
        self.square = Square
        self.piece = Piece

class Position:

    piece_dict = dict() # probably a better way, a dict of square: piece
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
            if piece > 0 and piece < 14: 
                self.piece_dict[e] = Piece(square=e, piece=piece))

        self.white_ks, self.white_qs = 'K' in castling, 'Q' in castling
        self.black_ks, self.black_qs = 'k' in castling, 'q' in castling
    
    def gen(self):
        pseudo_legal_moves = list()
        for piece in self.piece_dict.values():

            if (piece.piece < 7) == self.active_color: # this took me like 30 mins to figure out basic if statement

                # major difference is that pawns move diff based on color
                if piece.piece % 6 == 1:
                    pass
                    
                elif piece.piece % 6 == 2:
                    pass

                elif piece.piece % 6 == 6:
                    pass

                else:
                    # sliding pieces over here
                    for d in directions[piece.piece]:
                        for i in range(1,9):
                            if self.board[piece.square + i * d] == 0: # checking if empty square
                                pass
                            elif self.board[piece.square + i * d] != 13 or (self.board[piece.square + i * d] < 7) == active_color): # checking if out of board or if same piece
                                break
                            else:
                                # this should be a capture
                                pass

