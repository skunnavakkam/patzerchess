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

    board=[]
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
        pieces = elements[0]
        color = elements[1]
        castling = elements[2]
        ep = elements[3]
        fm = elements[5]
        hm = elements[4]

        self.is_white = (color == 'w')
        self.cwk, self.cwq, self.cbk, self.cbq = 'K' in castling, 'Q' in castling, 'k' in castling, 'q' in castling
        self.fm = int(fm)
        self.hm = int(hm)
        self.ep = ep if ep != '-' else None

        piece_dict = {'P':1,'N':2,'K':3,'B':4,'R':5,'Q':6,'p':9,'n':10,'k':11,'b':12,'r':13,'q':14}

        for row in pieces.split('/'):
            for piece in row:
                if piece.isdigit():
                    self.board.extend([0] * int(piece))
                
                else:
                    self.board.append(piece_dict[piece])
            
            self.board.extend([15] * 8)
    
        print(len(self.board))

    def _isattacked(self, square) -> bool:
        pass

    def _gen(self) -> tuple:

        pseudo_legal_moves = list()
        captures = list()

        for square, piece in enumerate(self.board): # i can't really save both my sanity and the time that it takes to go over blank squares so im sacrificng some efficieny
                        
            if piece == 0 or piece == 15:
                continue # continues if its 0 or 15

            for d in directions[piece]:
                for i in range(1,8):

                    if (square + d * i) & 0x88: 
                        break # out of bounds, don't have to table lookup

                     # we wnat to try to avoid lookup
                    target_square = square + d * i
                    target_destination = self.board[target_square]

                    if (piece ^ target_destination) >= 8: # i think this should be a catpurr
                        captures.append((square, target_square, piece))
                        break

                    elif target_destination == 0: # i think this should be an empty square
                        if piece == 1 or piece == 9:
                            if piece < 0x10 or piece > 0x67:
                                pseudo_legal_moves.append((square, target_square, 0b0010 + (piece & 1000)))
                                pseudo_legal_moves.append((square, target_square, 0b0100 + (piece & 1000)))
                                pseudo_legal_moves.append((square, target_square, 0b0101 + (piece & 1000)))
                                pseudo_legal_moves.append((square, target_square, 0b0110 + (piece & 1000)))
                        else:
                            pseudo_legal_moves.append((square, target_square, piece))

                    if not is_sliding_piece(piece):
                        break

        return (captures, pseudo_legal_moves)