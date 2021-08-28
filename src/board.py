
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
    2: (N + N + W, S + S + W, W + W + S, W + W + N, N + N + E, S + S + E, E + E + S, E + E + N),
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
    king_in_check = bool()
    
    # wc = white castle, bc = black castle, ep = enpassant, hm & fm = half and full move clocks
    def __init__(self, board, active_color, castling, ep, hm, fm):

        self.board, self.active_color, self.ep, self.hm, self.fm = board, active_color, ep, hm, fm  

        for e, piece in enumerate(board):
            if piece > 0 and piece < 14: 
                self.piece_dict[e] = Piece(Square=e, Piece=piece)

        self.white_ks, self.white_qs = 'K' in castling, 'Q' in castling
        self.black_ks, self.black_qs = 'k' in castling, 'q' in castling

    def check_if_square_attacked(self, square):
        is_attacked = bool()

        if self.active_color:
            if self.board[square + N + E] == 7 or self.board[square + N + W] == 7: # pawn
                return True
            
            for d in directions[2]: # horsey
                if self.board[square + d] == 8:
                    return True
                    
            for d in directions[3]: # bihop
                for i in range(1,9):
                    if self.board[square + d * i] != 0:
                        if self.board[square + d * i] == 9 or self.board[square + d * i] == 11:
                            return True
                        break

            for d in directions[4]: # rock + queen
                for i in range(1,9):
                    if self.board[square + d * i] != 0:
                        if self.board[square + d * i] == 10 or self.board[square + d * i] == 11:
                            return True
                        break

            for d in directions[5]:
                if self.board[square + d * i] == 12:
                    return True

        else:
            if self.board[square + S + E] == 7 or self.board[square + S + W] == 7: # pawn
                return True
            
            for d in directions[2]: # horsey
                if self.board[square + d] == 2:
                    return True
                    
            for d in directions[3]: # bihop
                for i in range(1,9):
                    if self.board[square + d * i] != 0:
                        if self.board[square + d * i] == 3 or self.board[square + d * i] == 5:
                            return True
                        break

            for d in directions[4]: # rock + queen
                for i in range(1,9):
                    if self.board[square + d * i] != 0:
                        if self.board[square + d * i] == 4 or self.board[square + d * i] == 5:
                            return True
                        break

            for d in directions[5]:
                if self.board[square + d * i] == 6:
                    return True
            
        return False

    def gen_out_of_check(self):
        pseudo_legal_moves = list()
        for piece in self.piece_dict.values():

            if (piece.piece < 7) == self.active_color: # this took me like 30 mins to figure out basic if statement

                # major difference is that pawns move diff based on color, and also promotion rules
                if piece.piece % 6 == 1:

                    pd = N # pawn direction

                    if piece.piece == 1:
                        pd = N

                    else:
                        pd = S

                    if self.board[piece.square + pd] == 0:
                        pseudo_legal_moves.append((piece.square, piece.square + 1))
                            # important to build in a promotion function when you make the move

                    if self.board[piece.square + pd + E] != 0 and self.board[piece.square + pd + E] != 13 and not ((self.board[piece.square + pd + E] < 7) == self.active_color):
                        # i think this should be a capture as well omegalul
                        pseudo_legal_moves.append((piece.square, piece.square + pd + E))

                    if self.board[piece.square + pd + W] != 0 and self.board[piece.square + pd + W] != 13 and not ((self.board[piece.square + pd + W] < 7) == self.active_color):
                        pseudo_legal_moves.append((piece.square, piece.square + pd + W))

                    if self.board[piece.square + pd + pd] == 0 and piece.square//10 == 2 and self.board[piece.square + pd] == 0:
                        pseudo_legal_moves.append((piece.square, piece.square + pd + pd))

                
                # horsey don't slide, and in addition don't care if their paths are being blocked
                elif piece.piece % 6 == 2:
                    for d in directions[piece.piece % 6]:

                        target_dest = piece.square + d

                        if target_dest > 99 or target_dest < 0:
                            continue

                        if (self.board[target_dest] == 0 or (self.board[target_dest] < 7 == self.active_color)) and self.board[target_dest] != 13:
                            pseudo_legal_moves.append((piece.square, target_dest))
        


                # kings have to be able to castle and don't slide
                # the repo im referencing doesn't check if the king is in check and just plays the move
                # but that makes it so the comp will have to calculate extra variations

                elif piece.piece % 6 == 0:

                    # traditional moves
                    for d in directions[5]:
                        if self.board[target_dest] == 0: # checking if empty square
                            pseudo_legal_moves.append((piece.square, target_dest))
                        elif self.board[target_dest] == 13 or ((self.board[target_dest] < 7) == self.active_color): # checking if out of board or if same piece
                            # we don't want to bother generating a piece if it overlaps with  
                            break
                        else:
                            # this should be a capture, so that means end the move generation for this piece once you have generated this move
                            pseudo_legal_moves.append((piece.square, target_dest))
                            break

                    # need to check for castle
                    if self.active_color:
                        # will be white
                        if self.white_ks:
                            pass
                        if self.white_qs:
                            pass
                    else:
                        # will be black
                        if self.black_qs:
                            pass
                        if self.black_ks:
                            pass

                else:
                    # sliding pieces over here
                    for d in directions[piece.piece % 6]:
                        for i in range(1,9):

                            target_dest = piece.square + i * d

                            if self.board[target_dest] == 0: # checking if empty square
                                pseudo_legal_moves.append((piece.square, target_dest))
                            elif self.board[target_dest] == 13 or ((self.board[target_dest] < 7) == self.active_color): # checking if out of board or if same piece
                                # we don't want to bother generating a piece if it overlaps with  
                                break
                            else:
                                # this should be a capture, so that means end the move generation for this piece once you have generated this move
                                pseudo_legal_moves.append((piece.square, target_dest))
                                break
                                
        return pseudo_legal_moves
                

    def gen_in_check(self):
        # no point generating all the possible pseudo-legal moves if you already know that you are in check
        pass


