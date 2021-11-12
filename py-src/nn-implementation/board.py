
import chess

Bitboard = int
Square = int

BB_QUEENSIDE = BB_FILE_A | BB_FILE_B | BB_FILE_C | BB_FILE_D
BB_KINGSIDE = BB_FILE_E | BB_FILE_F | BB_FILE_G | BB_FILE_H

BB_WHITESIDE = BB_RANK_1 | BB_RANK_2 | BB_RANK_3 | BB_RANK_4
BB_BLACKSIDE = BB_RANK_5 | BB_RANK_6 | BB_RANK_7 | BB_RANK_8


class Node:

    def __init__(self, board: SmartBoard) :

        # Moves that won't be masked
        self._legal_moves = 


# References
# https://www.chess.com/article/view/how-to-evaluate-a-position by Jeremy Silman
class SmartBoard(chess.Board):


    def image(self) -> []:

        turn = self.turn

        weak_complex = self._weak_complex(turn)
        opponent_weak_complex = self._weak_complex(not turn)

        king_pawn_shield, king_attackers = self._king_vicinity(turn)
        opponent_king_pawn_shield, opponent_king_attackers = _king_vicinity(not turn)

        pawn_tension = self._pawn_tension(turn)


    ##### Returns a bitboard of the color that are less controlled by our pawns #####
    ##### might change to BOOL in the future #####
    def _weak_complex(self, color) -> Bitboard:
        
        pawns = self.pawns[color]
        num_light_square_pawns = chess.popcount(pawns & chess.BB_LIGHT_SQUARES)
        num_dark_square_pawns = chess.popcount(pawns & chess.BB_DARK_SQUARES)

        if (num_light_square_pawns - num_dark_square_pawns) > num_dark_square_pawns:
            # the number of light squares is more than twice of the dark squares
            # dark squares are weak

            return chess.BB_DARK_SQUARES

        elif (num_dark_square_pawns - num_light_square_pawns) > num_light_square_pawns:
            # the number of dark squares is more than twice of the light square
            # light squares are weak

            return chess.BB_LIGHT_SQUARES


    def _king_vicinity(self, color) -> tuple :
        # locating quadrant
        # gets king square
        # from king square, gets file and rank
        # uses that to locate the quadrant
        king = self.king(color)
        king_file = king & 0b111
        king_rank = king >> 3

        file_mask = BB_KINGSIDE if king_file > 3 else BB_QUEENSIDE
        rank_mask = BB_BLACKSIDE if rank > 3 else BB_WHITESIDE

        quadrant_mask = file_mask & rank_mask

        # kings pawns
        pawn_shield = self.pawns & self.occupied_co[color] & quadrant_mask
        attackers = self.occupied_co[not color] & quadrant_mask

        return pawn_shield, attackers


    ##### Returns a Bitboard of pawns that can capture each other on their next ply #####
    def _pawn_tension(self) -> Bitboard:

        white_pawns = self.pawns & self.occupied_co[chess.WHITE]
        black_pawns = self.pawns & self.occupied_co[chess.BLACK]

        # only need to check what white can attack
        captures_west = ((white_pawns & ~chess.BB_FILE_A) << 7) & black_pawns
        pawns_capturing_west = captures_west >> 7

        captures_east = ((white_pawns & ~chess.BB_FILE_H) << 9) & black_pawns
        pawns_capturing_east = captures_east >> 9

        return (captures_west | pawns_capturing_west | captures_east | pawns_capturing_east)