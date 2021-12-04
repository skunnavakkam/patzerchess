
import chess
import numpy as np

_weak_square_mask = 0xff000000ffffffff
_central_piece_mask = 0x3c3c3c000000

class Board(chess.Board):

    def image(self):
        
        if not self.turn:
            return self.mirror().image()

        image = np.array(dtype=np.int16)

        # weak squares for the opponent
        image.append(self._weak_squares())

        # pawn tension
        image.append(self._pawn_tension())

        return image

    
    # returns weak_squares for the opponent
    def _weak_squares(self):

        mask = _weak_square_mask

        opp_pawns = self.pawns & self.occupied_co[False]

        attacks_left = (opp_pawns & ~chess.BB_FILE_A) >> 9
        attacks_right = (opp_pawns & ~chess.BB_FILE_H) >> 7
        one_square_attacks = attacks_left & attacks_right

        opp_pawns = opp_pawns >> 8
        attacks_left = (opp_pawns & ~chess.BB_FILE_A) >> 9
        attacks_right = (opp_pawns & ~chess.BB_FILE_H) >> 7
        two_square_attacks = attacks_left & attacks_right

        weak_squares = (one_square_attacks | two_square_attacks | mask) # leaves weak squares as 0s

        return weak_squares

    def _pawn_tension(self):
        
        white_pawns = self.pawns & self.occupied_co[chess.WHITE]
        black_pawns = self.pawns & self.occupied_co[chess.BLACK]

        # only need to check what white can attack
        captures_west = ((white_pawns & ~chess.BB_FILE_A) << 7) & black_pawns
        pawns_capturing_west = captures_west >> 7

        captures_east = ((white_pawns & ~chess.BB_FILE_H) << 9) & black_pawns
        pawns_capturing_east = captures_east >> 9

        return (captures_west | pawns_capturing_west | captures_east | pawns_capturing_east)        

    def good_pieces(self):

        # doing for white
        good_knights = self.knights & self.occupied_co[chess.WHITE] & _central_piece_mask
        fixed_pawns = ((self.pawns << 8) & self.pawns)
        fixed_pawns |= (fixed_pawns >> 8)

        pawns = fixed_pawns & self.occupied_co[chess.WHITE]
        

    def is_endgame(self) -> bool: 
        return (chess.popcount(self.occupied) <= 10)
