# to see the source for this, look at https://www.chessprogramming.org/Bitboards
# Sudarshanagopal Kunnavakkam 8 September 2021
# try no to steal my code please

class Position:
    pieces = [0] * 12
    hm = 0
    fm = 0
    castling = ""
    ep = None
    player = ""

    def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> None:

        pieces_to_list = {
            'p':0,'n':1,'b':2,'r':3,'q':4,'k':5,'P':6,'N':7,'B':8,'R':9,'Q':10,'K':11
        }

        starting_position = self.parsefen(fen)

        meta_data = fen.split(' ')
        self.player, self.castling, self.hm, self.fm = meta_data[1], meta_data[2], int(meta_data[4]), int(meta_data[5])

        for square, piece in enumerate(starting_position):

            if piece == ' ':
                continue

            self.pieces[pieces_to_list[piece]] ^= 1 << square


    def parsefen(self, fen):
        
        position = []

        if fen == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1":
            position = (
            'r','n','b','q','k','b','n','r',
            'p','p','p','p','p','p','p','p',
            ' ',' ',' ',' ',' ',' ',' ',' ',
            ' ',' ',' ',' ',' ',' ',' ',' ',
            ' ',' ',' ',' ',' ',' ',' ',' ',
            ' ',' ',' ',' ',' ',' ',' ',' ',
            'P','P','P','P','P','P','P','P',
            'R','N','B','Q','K','B','N','R'
            )
            return position
        
        elements = fen.split(' ')
        pieces = elements[0]

        for i in pieces:
            if i == "/":
                continue

            elif i.isdigit():
                for m in range(int(i)):
                    position.append(' ')

            else:
                position.append(i)

        return(tuple(position))

    def gen(self):
        # work on this later
        pass