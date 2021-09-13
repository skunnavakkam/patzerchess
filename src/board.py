# to see the source for this, look at https://en.wikipedia.org/wiki/0x88
# Sudarshanagopal Kunnavakkam 8 September 2021
# try no to steal my code please
# i really reccomend you have rainbow brackets or smth similar installed
# im so tempted to make everything bitwise, but i also want people to be able to read my code

'''
    White   Black

P   0001    1001
N   0010    1010
K   0011    1011
B   0100    1100
R   0101    1101
Q   0110    1110

empty = 0000

X = Piece
Y = Target

capture:
if (X ^ Y) > 1000

empty:
if (X ^ Y) == X

own piece:
if (X ^ Y) < 1000


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

    bitboards=[0] * 12
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
                self.bitboards[piece_dict[piece]] ^= 1 << square

    def _gen(self):

        for piece,board in enumerate(self.bitboards):
            
            if board == 0:
                continue