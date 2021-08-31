
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

directions = {
    2: (N + N + W, S + S + W, W + W + S, W + W + N, N + N + E, S + S + E, E + E + S, E + E + N),
    3: (N+W, S+W, N+E, S+E), # bishop
    4: (N, S, W, E),
    5: (N, S, W, E, N+W, S+W, N+E, S+E)
}



class Position:

    castling = [False, False, False, False]
    ep = int()
    hm = int()
    fm = int()
    board = list()
    active_color = bool() # true if w 
    king = None
    
    # wc = white castle, bc = black castle, ep = enpassant, hm & fm = half and full move clocks
    def __init__(self, board, active_color, castling, ep, hm, fm):

        self.board, self.active_color, self.ep, self.hm, self.fm = board, active_color, ep, hm, fm  
        self.castling[0], self.castling[1], self.castling[2], self.castling[3] = 'K' in castling, 'Q' in castling, 'k' in castling, 'q' in castling

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

    def move(self, move): # the piece would be equal to the promotion value in the case of promotion

        start = move[0]
        end = move [1]
        piece = move[2]


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

        self.board[start] = 0
        self.board[end] = piece

        if not is_capture and not is_pawn_move:
            self.hm += 1
            if not self.active_color:
                self.fm += 1
        

        
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