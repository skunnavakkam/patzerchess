# to see the source for this, look at https://en.wikipedia.org/wiki/0x88
# Sudarshanagopal Kunnavakkam 8 September 2021
# try no to steal my code please

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

        for square, piece in enumerate(pieces):
            if square % 8 == 0:
                

            if piece == '/':
                continue

            