
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

N, S, E, W = 10, -10, -1, 1

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
    king = None
    
    # wc = white castle, bc = black castle, ep = enpassant, hm & fm = half and full move clocks
    def __init__(self, board, active_color, castling, ep, hm, fm):

        self.board, self.active_color, self.ep, self.hm, self.fm = board, active_color, ep, hm, fm  

        for e, piece in enumerate(board):
            if piece > 0 and piece < 13: 
                self.piece_dict[e] = Piece(Square=e, Piece=piece)

        self.white_ks, self.white_qs = 'K' in castling, 'Q' in castling
        self.black_ks, self.black_qs = 'k' in castling, 'q' in castling

    def is_square_attacked(self, square):

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

            for d in directions[5]: # big daddy king
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

            for d in directions[5]: # big daddy king
                if self.board[square + d * i] == 6:
                    return True
            
        return False

    def gen(self):
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

                        if piece.square + pd // 10 == 9:
                            pseudo_legal_moves.append(piece.square, piece.square + pd, )
                        else: 
                            pseudo_legal_moves.append((piece.square, piece.square + pd))

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
                            pseudo_legal_moves.append((piece.square, target_dest, piece.piece))
        


                # kings have to be able to castle and don't slide
                # the repo im referencing doesn't check if the king is in check and just plays the move
                # but that makes it so the comp will have to calculate extra variations

                elif piece.piece % 6 == 0:

                    ks_directions = [E, E + E]
                    qs_directions = [W, W + W, W + W + W]

                    square = piece.square

                    # traditional moves
                    for d in directions[5]:

                        target_dest = square + d

                        if self.board[target_dest] == 0: # checking if empty square
                            pseudo_legal_moves.append((piece.square, target_dest, piece.piece))
                        elif self.board[target_dest] == 13 or ((self.board[target_dest] < 7) == self.active_color): # checking if out of board or if same piece
                            # we don't want to bother generating a piece if it overlaps with  
                            break
                        else:
                            # this should be a capture, so that means end the move generation for this piece once you have generated this move
                            pseudo_legal_moves.append((piece.square, target_dest, piece.piece))
                            break

                    
                    current_ks = bool()
                    current_qs = bool()
                    # need to check for castle
                    if self.active_color:
                        current_ks = self.white_ks
                        current_qs = self.white_qs

                    else: 
                        current_qs = self.black_qs
                        current_ks = self.black_ks

                    if current_ks:

                        can_ks = True

                        for d in ks_directions:

                            if self.is_square_attacked(square + d) or self.board[square + d] != 0:
                                can_ks = False
                                break

                        if can_ks:
                            pseudo_legal_moves.append((square, square + E + E, piece.piece))

                    if current_qs:
                        
                        can_qs = True

                        for d in qs_directions:

                            if self.is_square_attacked(square + d) or self.board[square + d] != 0:
                                can_qs = False
                                break

                        if can_ks:
                            pseudo_legal_moves.append((square, square + W + W + W, piece.piece))                         

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

    def move(self, start, end, piece): # the piece would be equal to the promotion value in the case of promotion

        is_pawn_move = bool()
        is_capture = bool()
        is_promotion = bool()

        if self.active_color:
            
            if self.board[start] == 6:
                self.white_ks = False
                self.white_qs = False
            if self.board[start] == 4:
                if start == 11 and self.white_qs:
                    self.white_qs = False
                if start == 18 and self.white_ks:
                    self.white_ks = False
        
        else:
            if self.board[start] == 12:
                self.white_ks = False
                self.white_qs = False
            if self.board[start] == 10:
                if start == 11 and self.white_qs:
                    self.white_qs = False
                if start == 18 and self.white_ks:
                    self.white_ks = False

        if self.board[start] % 6 == 1:

            is_pawn_move = True

            is_promotion = piece != self.board[start]

            if abs(end - start) == 20:
                self.ep = start - 10
                
                if self.board[start] == 1:
                    self.ep = start + 10

        if end in self.piece_dict:
            is_capture = True
            self.piece_dict.pop(end)

        self.piece_dict[start].square = end

        self.board[end] = piece

        self.board[start] = 0

        
    def __repr__(self) -> str:
        
        to_return = "\n"

        # white pieces look black on when changing between light and dark theme, but gonna assume coders use dark
        dark_theme = [".", "♟︎", "♞", "♝", "♜", "♛", "♚", "♙", "♘", "♗", "♖", "♕", "♔"]

        piece_counter = 0

        for piece in self.board[::-1]: # wiithout the [::-1] it displays it as being blacks move
            if piece != 13:
                piece_counter += 1
                to_return += "  "
                to_return += dark_theme[piece]
                to_return += "  "

            if piece_counter == 8:
                to_return += "\n\n"
                piece_counter = 0
        
        # removing last two \n from the board
        to_return = to_return[:len(to_return) - 1]

        return to_return