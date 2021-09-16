# to see the source for this, look at https://en.wikipedia.org/wiki/0x88
# Sudarshanagopal Kunnavakkam 8 September 2021
# try no to steal my code please
# i really reccomend you have rainbow brackets or smth similar installed
# im so tempted to make everything bitwise, but i also want people to be able to read my code

'''
noWe         nort         noEa
        -9    -8    -7
            \  |  /
west    -1 <-  0 -> +1    east
            /  |  \
        +7    +8    +9
soWe         sout         soEa
'''

N, S, E, W = -10, 10, 1, -1
directions = {
    1:(N,), # p (just having the pawns direction here, and going to handle pawns later)
    2:(N+N+E, E+N+E, E+S+E, S+S+E, S+S+W, W+S+W, W+N+W, N+N+W), # n
    3:(N, E, S, W, N+E, S+E, S+W, N+W), # k
    4:(N+E, S+E, S+W, N+W), # b
    5:(N, E, S, W), # r
    6:(N, E, S, W, N+E, S+E, S+W, N+W), # q
    9:(S,),
    10:(N+N+E, E+N+E, E+S+E, S+S+E, S+S+W, W+S+W, W+N+W, N+N+W),
    11:(N, E, S, W, N+E, S+E, S+W, N+W),
    12:(N+E, S+E, S+W, N+W),
    13:(N, E, S, W),
    14:(N, E, S, W, N+E, S+E, S+W, N+W)
} # probably inefficient use of memory but idc about the computer
is_sliding_piece = lambda x: (x & 0b0111) > 3 # more efficient mod operator, also im trying to flex



class Position:

    WP = WN = WB = WR = WQ = WK = BP = BN = BB = BR = BQ = BK = 0
    black_board = 0 # storing these values to make checking for moves and things easier
    white_board = 0 # not sure if this is necessary though
    is_white = True
    hm = 0
    fm = 0
    ep = None
    cwk = False
    cwq = False
    cbk = False
    cbq = False


    def __init__(self,fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):

        elements = fen.split(' ')
        piece_list = elements[0].replace('/','')
        color = elements[1]
        castling = elements[2]
        ep = elements[3]
        fm = elements[5]
        hm = elements[4]
        piece_string = str()

        self.is_white = (color == 'w')
        self.cwk, self.cwq, self.cbk, self.cbq = 'K' in castling, 'Q' in castling, 'k' in castling, 'q' in castling
        self.fm = int(fm)
        self.hm = int(hm)
        self.ep = ep if ep != '-' else None

        piece_dict = {'P':0,'N':1,'K':2,'B':3,'R':4,'Q':5,'p':6,'n':7,'k':8,'b':9,'r':10,'q':11}

        for piece in piece_list:
            if piece.isdigit():
                piece_string += ' ' * int(piece)
            else:
                piece_string += piece

        for square, piece in enumerate(piece_string):
            if piece != ' ':


                if piece == 'P':
                    self.WP ^= 1 << square
                if piece == 'N':
                    self.WN ^= 1 << square
                if piece == 'B':
                    self.WB ^= 1 << square
                if piece == 'R':
                    self.WR ^= 1 << square
                if piece == 'Q':
                    self.WQ ^= 1 << square
                if piece == 'K':
                    self.WK ^= 1 << square


                if piece == 'p':
                    self.BP ^= 1 << square
                if piece == 'n':
                    self.BN ^= 1 << square
                if piece == 'b':
                    self.BB ^= 1 << square
                if piece == 'r':
                    self.BR ^= 1 << square
                if piece == 'q':
                    self.BQ ^= 1 << square
                if piece == 'k':
                    self.BK ^= 1 << square


                if piece.isupper():
                    self.white_board ^= 1 << square
                else:
                    self.black_board ^= 1 << square

    def _gen_out_of_check(self):
        
        N = -8
        S = 8
        E = 1
        W = -1
        NE = N + E
        NW = N + W
        SE = S + E
        NOT_A = 0b1111111011111110111111101111111011111110111111101111111011111110
        NOT_H = 0b0111111101111111011111110111111101111111011111110111111101111111
        RANK3 = 0b0000000000000000111111110000000000000000000000000000000000000000
        RANK7 = 0b0000000000000000000000000000000000000000111111110000000000000000

        if self.WP:

            single_move = (self.WP >> 8) & ~self.black_board
            pawn_attacks = (  ((self.WP >> 7) & NOT_H)  |  ((self.WP >> 9) & NOT_A)  ) & self.black_board # fuck enpassant
            double_move = ((single_move & RANK3) >> 8) & ~self.black_board # shifting pawns from the second rank one square in single_move, and another in double_move

        if self.WN:
            pass


