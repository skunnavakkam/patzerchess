# to see the source for this, look at https://en.wikipedia.org/wiki/0x88
# Sudarshanagopal Kunnavakkam 8 September 2021
# try no to steal my code please
# i really reccomend you have rainbow brackets or smth similar installed

'''
    White   Black

P   0001    1001
N   0010    1010
B   0011    1011
R   0100    1100
Q   0101    1101
K   0110    1110

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

        piece_dict = {'P':1,'N':2,'B':3,'R':4,'Q':5,'K':6,'p':9,'n':10,'b':11,'r':12,'q':13,'k':14}

        for row in pieces.split('/'):
            for piece in row:
                if piece.isdigit():
                    self.board.append([0] * int(piece))
                
                else:
                    self.board.append(piece_dict[piece])
            
            self.board.append([15] * 8)

                