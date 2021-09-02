
# if you want to see an actual decent chess engine, please take a look at sunfish, the inspiration and reference for this project

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

directions = {
    2: (N + N + W, S + S + W, W + W + S, W + W + N, N + N + E, S + S + E, E + E + S, E + E + N),
    3: (N+W, S+W, N+E, S+E), # bishop
    4: (N, S, W, E),
    5: (N, S, W, E, N+W, S+W, N+E, S+E)
}


# stuff for evaluation
piece = { 1: 100, 2: 280, 3: 320, 4: 479, 5: 929, 0: 60000 }
pst = {
    1: (   0,   0,   0,   0,   0,   0,   0,   0,
            78,  83,  86,  73, 102,  82,  85,  90,
             7,  29,  21,  44,  40,  31,  44,   7,
           -17,  16,  -2,  15,  14,   0,  15, -13,
           -26,   3,  10,   9,   6,   1,   0, -23,
           -22,   9,   5, -11, -10,  -2,   3, -19,
           -31,   8,  -7, -37, -36, -14,   3, -31,
             0,   0,   0,   0,   0,   0,   0,   0),
    2: ( -66, -53, -75, -75, -10, -55, -58, -70,
            -3,  -6, 100, -36,   4,  62,  -4, -14,
            10,  67,   1,  74,  73,  27,  62,  -2,
            24,  24,  45,  37,  33,  41,  25,  17,
            -1,   5,  31,  21,  22,  35,   2,   0,
           -18,  10,  13,  22,  18,  15,  11, -14,
           -23, -15,   2,   0,   2,   0, -23, -20,
           -74, -23, -26, -24, -19, -35, -22, -69),
    3: ( -59, -78, -82, -76, -23,-107, -37, -50,
           -11,  20,  35, -42, -39,  31,   2, -22,
            -9,  39, -32,  41,  52, -10,  28, -14,
            25,  17,  20,  34,  26,  25,  15,  10,
            13,  10,  17,  23,  17,  16,   0,   7,
            14,  25,  24,  15,   8,  25,  20,  15,
            19,  20,  11,   6,   7,   6,  20,  16,
            -7,   2, -15, -12, -14, -15, -10, -10),
    4: (  35,  29,  33,   4,  37,  33,  56,  50,
            55,  29,  56,  67,  55,  62,  34,  60,
            19,  35,  28,  33,  45,  27,  25,  15,
             0,   5,  16,  13,  18,  -4,  -9,  -6,
           -28, -35, -16, -21, -13, -29, -46, -30,
           -42, -28, -42, -25, -25, -35, -26, -46,
           -53, -38, -31, -26, -29, -43, -44, -53,
           -30, -24, -18,   5,  -2, -18, -31, -32),
    5: (   6,   1,  -8,-104,  69,  24,  88,  26,
            14,  32,  60, -10,  20,  76,  57,  24,
            -2,  43,  32,  60,  72,  63,  43,   2,
             1, -16,  22,  17,  25,  20, -13,  -6,
           -14, -15,  -2,  -5,  -1, -10, -20, -22,
           -30,  -6, -13, -11, -16, -11, -16, -27,
           -36, -18,   0, -19, -15, -15, -21, -38,
           -39, -30, -31, -13, -31, -36, -34, -42),
    0: (   4,  54,  47, -99, -99,  60,  83, -62,
           -32,  10,  55,  56,  56,  55,  10,   3,
           -62,  12, -57,  44, -67,  28,  37, -31,
           -55,  50,  11,  -4, -19,  13,   0, -49,
           -55, -43, -52, -28, -51, -47,  -8, -50,
           -47, -42, -43, -79, -64, -32, -29, -32,
            -4,   3, -14, -50, -57, -18,  13,   4,
            17,  30,  -3, -14,   6,  -1,  40,  18),
}

doubled_pawn_penalty = -30
isolated_pawn_penalty = -40
tripled_or_greater_penalty = -70 

class Position:

    castling = [False, False, False, False]
    ep = int()
    hm = int()
    fm = int()
    board = list()
    active_color = bool() # true if w 
    king = None
    pawn_structure = [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]] # [white, black]. each digit maps to a column and counts the number of pawns in that column
    score = 0
    
    # wc = white castle, bc = black castle, ep = enpassant, hm & fm = half and full move clocks
    def __init__(self, board, active_color, castling, ep, hm, fm):

        self.board, self.active_color, self.ep, self.hm, self.fm = board, active_color, ep, hm, fm  
        self.castling[0], self.castling[1], self.castling[2], self.castling[3] = 'K' in castling, 'Q' in castling, 'k' in castling, 'q' in castling

        for square, piece in enumerate(board):
            if piece == 1:
                self.pawn_structure[0][square % 10] = self.pawn_structure[0][square % 10] + 1
            elif piece == 6:
                self.pawn_structure[1][square % 10] = self.pawn_structure[0][square % 10] + 1


    def is_square_attacked(self, square, color_to_check):
        
        # Knight
        for d in directions[2]:
            if self.board[square + d] == (8 - color_to_check * 6):
                return True
        
        # King
        for d in directions[5]:
            if self.board[square + d] == (12 - color_to_check * 6):
                return True
        
        # diagonal (Bishop + Queen)
        for d in directions[3]:
            for i in range(1,9):
                if self.board != 0:
                    if self.board[square + d] == (11 - color_to_check * 6) or self.board[square + d] == (9 - color_to_check * 6):
                        return True
                    break
        
        # straight (Rook + Queen)
        for d in directions[4]:
            for i in range(1,9):
                if self.board != 0:
                    if self.board[square + d] == (11 - color_to_check * 6) or self.board[square + d] == (10 - color_to_check * 6):
                        return True
                    break
        
        # pawns
        if color_to_check:
            if self.board[square + S + E] == 1 or self.board[square + S + W] == 1:
                return True
        else:
            if self.board[square + N + E] == 7 or self.board[square + N + W] == 7:
                return True

        return False

    def gen(self):
        pseudo_legal_moves = list()

        for square, piece in enumerate(self.board):

            if piece == 0 or piece == 13 or piece > 6 != self.active_color:
                continue # we don't care about things that aren't pieces

            elif piece % 6 == 1:

                pd = -10 + 20 * self.active_color # pawn direction

                for i in [pd + E, pd + W]:

                    print(square)

                    if self.board[square + i] > 6 or square + i == self.ep:
                        pseudo_legal_moves.append((square, square + i, piece))
                
                if self.board[square + pd] == 0:
                    if (square // 10 == (8 - 6 * self.active_color)) and self.board[square + pd + pd] == 0:
                        pseudo_legal_moves.append((square, square + pd + pd, piece)) # move two squares

                    if square // 10 == (80 - 60 * (not self.active_color)):
                        for i in range(2,6):
                            pseudo_legal_moves.append((square, square + pd, i))
                    
                    else: 
                        pseudo_legal_moves.append((square, square + pd, piece))
                
            elif piece % 6 == 2:

                for d in directions[2]:

                    if square + d > 99 or square + d < 0:
                        continue

                    if (self.board[square + d] == 0 or self.board[square + d] > 6 == self.active_color) and self.board[square + d] != 13:
                        pseudo_legal_moves.append((square, square + d, piece))

            elif piece % 6 == 0:

                for d in directions[5]:
                    if self.board[square + d] == 0 or self.board[square + d] > 6 == self.active_color:
                        pseudo_legal_moves.append((square, square + d, piece))

                # king and queenside castling
                ks_directions = [E, E + E]
                qs_directions = [W, W + W, W + W + W]

                can_ks = bool()
                can_qs = bool()

                for d in ks_directions:
                    can_ks = can_ks and self.is_square_attacked(square + d, not self.active_color)

                for d in qs_directions:
                    can_qs = can_qs and self.is_square_attacked(square + d, not self.active_color)

                if can_ks and self.castling[2 - (2 * self.active_color)]:
                    pseudo_legal_moves.append((square, square + E + E, piece))
                
                if can_qs and self.castling[3 - (2 * self.active_color)]:
                    pseudo_legal_moves.append((square, square + W + W + W, piece))

            
            else:

                for d in directions[piece % 6]:
                    for i in range(1,8):

                        target_dest = square + i * d
                        

                        if self.board[target_dest] == 0:
                            #print(self.board[target_dest])
                            # empty
                            pseudo_legal_moves.append((square, target_dest, piece))
                        elif (self.board[target_dest] > 6) != self.active_color or self.board[target_dest] == 13:
                            break
                        else:
                            pseudo_legal_moves.append((square, target_dest, piece))
                            break
              
        return pseudo_legal_moves

    # use this instead, it creates a duplicate for searching
    def move(self, move):
        to_return = self

        to_return._move(move)

        return to_return

    # don't use this to move piece
    def _move(self, start, end, piece): # the piece would be equal to the promotion value in the case of promotion

        is_pawn_move = bool()
        is_capture = bool()

        if piece % 6 == 0:
            self.castling[3 - (self.active_color * 2)] = self.castling[2-(self.active_color * 2)] = False
        if start == (88 - 70 * self.active_color) and self.castling[3-self.active_color * 2]:
            self.white_qs = False
        if start == (81 - 70 * self.active_color) and self.castling[2-self.active_color * 2]:
            self.white_ks = False

        if end == self.ep:
            self.board[end + 10 - (20 * self.active_color)] = 0

        if self.board[start] % 6 == 1:
            is_pawn_move = True
            if end - start == 20:
                self.ep = start + 10
            elif end - start == -20:
                self.ep = start - 10
            if abs(end - start) == 20:
                self.ep = start - ((end - start)/2)

        self.board[start] = 0
        self.board[end] = piece

        if not is_capture and not is_pawn_move:
            self.hm += 1
            if not self.active_color:
                self.fm += 1
        
    # this should be run before you make the move
    # literally ripped off of sunfish kekw
    def eval(self, start, end, piece):
        p, q = self.board[start], self.board[end]
        pawn_structure = self.pawn_structure
        score = 0


        if p % 6 == 1:
            pawn_structure[(p - 1)/6][start % 10] -= 1
        if piece % 6 == 1: # considering promotion
            pawn_structure[(p-1)/6][end % 10] += 1

        if piece < 7:
            score = pst[piece][end] - pst[p][start]
            if q != 0:
                # capture
                score += pst[q % 6][99-end]
        else: 
            score = pst[piece % 6][99 - end] - pst[p % 6][99 - start]




        
        # program a check to see if capture by getting the end square and the start square and checking if they're different
            


        
        
    def __repr__(self) -> str:
        
        to_return = "\n"

        # white pieces look black on when changing between light and dark theme, but gonna assume coders use dark
        dark_theme = ["·", "♟︎", "♞", "♝", "♜", "♛", "♚", "♙", "♘", "♗", "♖", "♕", "♔"]

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