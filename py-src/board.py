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

    # just a debugging tool that allows me to print a bit board as a chess board
    def as_board(self, bitboard):
        return_string = ""
        bb = bin(bitboard)[2:][::-1]
        for square, bit in enumerate( (bb + ((64 - len(bb)) * "0")) ):
            return_string += bit
            return_string += " "
            if square % 8 == 7:
                return_string += "\n"
        return return_string

    def _gen_out_of_check(self):
        
        N = -8
        S = 8
        E = 1
        W = -1
        NE = N + E
        NW = N + W
        SE = S + E
        
        # general masks
        NOT_A  = 0b1111111011111110111111101111111011111110111111101111111011111110
        NOT_H  = 0b0111111101111111011111110111111101111111011111110111111101111111
        NOT_1  = 0b1111111111111111111111111111111111111111111111111111111100000000
        NOT_8  = 0b0000000011111111111111111111111111111111111111111111111111111111

        # pawn masks
        RANK3  = 0b0000000000000000111111110000000000000000000000000000000000000000
        RANK6  = 0b0000000000000000000000000000000000000000111111110000000000000000

        # knight masks
        NOT_AB = 0b1111110011111100111111001111110011111100111111001111110011111100
        NOT_GH = 0b0011111100111111001111110011111100111111001111110011111100111111

        WB_board = self.black_board | self.white_board
        WB_board_flip = ~WB_board
        white_board_flip = ~self.white_board
        black_board_flip = ~self.black_board


        if self.WP:

            single_move = (self.WP >> 8) & WB_board_flip
            pawn_attacks = ((self.WP & NOT_H) >> 7) | ((self.WP & NOT_A) >> 9)
            double_move = ((single_move & RANK3) >> 8) & WB_board_flip
            pawn_captures = pawn_attacks & self.black_board

        if self.WN:
            # variables named as 
            # 2 move direction 1 move direction
            # moving two squares N and 1 square E would be NE
        
            NE_moves = (self.WN >> 15) & NOT_A & white_board_flip
            NW_moves = (self.WN >> 17) & NOT_H & white_board_flip
            
            EN_moves = (self.WN >> 6) & NOT_AB & white_board_flip
            ES_moves = (self.WN << 10) & NOT_AB & white_board_flip

            SE_moves = (self.WN << 17) & NOT_A & white_board_flip
            SW_moves = (self.WN << 15) & NOT_H & white_board_flip

            WN_moves = (self.WN >> 10) & NOT_GH & white_board_flip
            WS_moves = (self.WN << 6) & NOT_GH & white_board_flip

            knight_moves = NE_moves | NW_moves | EN_moves | ES_moves \
                            | SE_moves | SW_moves | WN_moves | WS_moves
        if self.WK:
            
            E_move = (self.WK << 1) & NOT_A
            W_move = (self.WK >> 1) & NOT_H

            king_horizontal = E_move | self.WK | W_move

            king_moves = ((king_horizontal & NOT_8) << 8) | E_move | W_move | ((king_horizontal & NOT_1) >> 8)


        # --------------------------------------Sliding Pieces--------------------------------------      

        mod8 = lambda x: x & 0b111
        file_mask = (0x101010101010101, 0x202020202020202, 0x404040404040404, 0x808080808080808,
                    0x1010101010101010, 0x2020202020202020, 0x4040404040404040, 0x8080808080808080)
        rank_mask = (0xFF00000000000000, 0xFF000000000000, 0xFF0000000000, 0xFF00000000, 
                    0xFF000000, 0xFF0000, 0xFF00, 0xFF)
        # trying to avoid looking up these tuples
        # fuckkkkk i need to do a lookup table

        if self.WR:
            
            rank_moves = 0
            file_moves = 0

            for i in range(8):
                r = rank_mask[i]
                f = file_mask[i]

                file_slider = self.WR & r
                rank_slider = self.WR & f

                print(self.as_board(f), i)

                if rank_slider:

                    o = WB_board & r

                    moves = ((o - 2 * rank_slider)) & r

                    rank_moves |= moves

                if file_slider:

                    o = WB_board & f

                    moves = (o-2 * file_slider) & f

                    file_moves |= moves
                
            rank_moves ^= WB_board
            file_moves ^= WB_board