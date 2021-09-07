
# if you want to see an actual decent chess engine, please take a look at sunfish, the reference for this project
# time taken = 30 to 40 micro seconds running at home

'''
board

[13,13,13,13,13,13,13,13,13,13,
 13, 4, 2, 3, 5, 6, 3, 2, 4,13,
 13, 1, 1, 1, 1, 1, 1, 1, 1,13,
 13, 0, 0, 0, 0, 0, 0, 0, 0,13,
 13, 0, 0, 0, 0, 0, 0, 0, 0,13,
 13, 0, 0, 0, 0, 0, 0, 0, 0,13,
 13, 0, 0, 0, 0, 0, 0, 0, 0,13,
 13, 7, 7, 7, 7, 7, 7, 7, 7,13,
 13,10, 8, 9,11,12, 9, 8,10,13,
 13,13,13,13,13,13,13,13,13,13]

the basic board representation, is an array. the array contains 100 elements. 
the "13" on the edge are to make checking for moves off the board, by checking if the
square that you plan to move to is "13". However, the "13" will probably be replaced by 
a different symbol in the code. "13" represents empty squares kek

| NUMBER | COLOR | PIECE
| 1      | white | pawn
| 2      | white | knightx
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

# stuff for generation
N, S, E, W = 10, -10, -1, 1
A1, H1, A8, H8 = 11, 18, 81, 88
directions = {
    2: (N + N + W, S + S + W, W + W + S, W + W + N, N + N + E, S + S + E, E + E + S, E + E + N),
    3: (N+W, S+W, N+E, S+E), # bishop
    4: (N, S, W, E),
    5: (N, S, W, E, N+W, S+W, N+E, S+E)
}

class Position:
    WP = WN = WB = WR = WQ = WK = BP = BN = BB = BR = BQ = BK = 0
    fm = 0
    hm = 0
    player = 0
    ep = None

    def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        start_position = (
        'r','n','b','q','k','b','n','r',
        'p','p','p','p','p','p','p','p',
        ' ',' ',' ',' ',' ',' ',' ',' ',
        ' ',' ',' ',' ',' ',' ',' ',' ',
        ' ',' ',' ',' ',' ',' ',' ',' ',
        ' ',' ',' ',' ',' ',' ',' ',' ',
        'P','P','P','P','P','P','P','P',
        'R','N','B','Q','K','B','N','R'
        )

        if fen != "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1":
            # parse fen here kekw
            # and set the start position to the parsed fen
            pass

        for square, piece in enumerate(start_position):
            if piece == 'r':
                self.BR += 2 ** square
            elif piece == 'n':
                self.BN += 2 ** square
            elif piece == 'b':
                self.BB += 2 ** square
            elif piece == 'q':
                self.BQ += 2 ** square
            elif piece == 'k':
                self.BK += 2 ** square
            elif piece == 'p':
                self.BP += 2 ** square
            elif piece == 'R':
                self.WR += 2 ** square
            elif piece == 'N':
                self.WN += 2 ** square
            elif piece == 'B':
                self.WB += 2 ** square
            elif piece == 'Q':
                self.WQ += 2 ** square
            elif piece == 'K':
                self.WK += 2 ** square
            elif piece == 'P':
                self.WP += 2 ** square
            

            