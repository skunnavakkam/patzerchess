
import chess
import numpy as np

from numpy import ulonglong

_weak_square_mask = 0xff000000ffffffff
_central_piece_mask = 0x3c3c3c000000

def bitarray(longlong):
    return np.asarray([((longlong >> x) & 0b1) for x in range(64)], dtype=np.bool_)

class Board(chess.Board):

    def aux_planes(self):
        castling = bitarray(self.castling_rights)
        ep = bitarray(1 << self.ep if self.ep is not None else 0)
        hm = np.full(64, self.halfmove_count, dtype=np.ubyte)
        
    def handpicked_planes(self):
        turn = self.turn
        good_pieces = self.good_pieces(turn)
        return np.array([bitarray(self._weak_squares(turn)),
                         bitarray(self._weak_square_mask(not turn)),
                         bitarray(self._pawn_tension()),
                         bitarray(good_pieces[0]),
                         bitarray(good_pieces[1])])

    def game_planes(self):
        return np.array([bitarray(self.kings),
                         bitarray(self.knights),
                         bitarray(self.bishops | self.queens),
                         bitarray(self.rooks | self.queens),
                         bitarray(self.occupied_co[True]),
                         bitarray(self.occupied_co[False])])
        
    
    # returns weak_squares for the opponent
    def _weak_squares(self, turn):

        mask = _weak_square_mask

        opp_pawns = self.pawns & self.occupied_co[not turn]

        attacks_left = (opp_pawns & ~chess.BB_FILE_A) >> 9
        attacks_right = (opp_pawns & ~chess.BB_FILE_H) >> 7
        one_square_attacks = attacks_left & attacks_right

        opp_pawns = opp_pawns >> 8
        attacks_left = (opp_pawns & ~chess.BB_FILE_A) >> 9
        attacks_right = (opp_pawns & ~chess.BB_FILE_H) >> 7
        two_square_attacks = attacks_left & attacks_right

        weak_squares = (one_square_attacks | two_square_attacks | mask) # leaves weak squares as 0s

        return ulonglong(weak_squares)

    def _pawn_tension(self):
        
        white_pawns = self.pawns & self.occupied_co[chess.WHITE]
        black_pawns = self.pawns & self.occupied_co[chess.BLACK]

        # only need to check what white can attack
        captures_west = ((white_pawns & ~chess.BB_FILE_A) << 7) & black_pawns
        pawns_capturing_west = captures_west >> 7

        captures_east = ((white_pawns & ~chess.BB_FILE_H) << 9) & black_pawns
        pawns_capturing_east = captures_east >> 9

        return ulonglong(captures_west | pawns_capturing_west | captures_east | pawns_capturing_east)        

    def good_pieces(self, turn):

        # doing for white
        good_knights = self.knights & self.occupied_co[turn] & _central_piece_mask
        fixed_pawns = ((self.pawns << 8) & self.pawns)
        fixed_pawns |= (fixed_pawns >> 8)

        pawns = fixed_pawns & self.occupied_co[turn]
        light_square_pawns = pawns & chess.BB_LIGHT_SQUARES
        num_light_square_pawns = chess.popcount(light_square_pawns)
        fixed_pawns_light_squares = ((chess.popcount(pawns) - num_light_square_pawns) > num_light_square_pawns)
        pawn_mask = chess.BB_DARK_SQUARES if fixed_pawns_light_squares else chess.BB_LIGHT_SQUARES
        good_bishop = (self.bishops & self.occupied_co[chess.WHITE]) & pawn_mask

        our_good_piece = ulonglong(good_knights | good_bishop)

        # doing for black
        good_knights = self.knights & self.occupied_co[not turn] & _central_piece_mask
        pawns = fixed_pawns & self.occupied_co[not turn]
        light_square_pawns = pawns & chess.BB_LIGHT_SQUARES
        num_light_square_pawns = chess.popcount(light_square_pawns)
        fixed_pawns_light_squares = ((chess.popcount(pawns) - num_light_square_pawns) > num_light_square_pawns)
        pawn_mask = chess.BB_DARK_SQUARES if fixed_pawns_light_squares else chess.BB_LIGHT_SQUARES
        good_bishop = (self.bishops & self.occupied_co[not turn]) & pawn_mask 

        their_good_pieces = ulonglong(good_knights | good_bishop)

        return our_good_piece, their_good_pieces
    
    def is_endgame(self) -> bool: 
        return (chess.popcount(self.occupied) <= 10)

