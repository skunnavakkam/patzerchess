import chess
import numpy as np


def bit_array(x):
    return list(map(int, "{:064b}".format(x)))


class Board(chess.Board):
    def image(self):

        game_planes = [
            bit_array(self.kings),
            bit_array(self.pawns),
            bit_array(self.knights),
            bit_array(self.queens | self.rooks),
            bit_array(self.queens | self.bishops),
            bit_array(self.occupied_co[True]),
            bit_array(self.occupied_co[False]),
        ]

        ep_array = np.zeros(64)
        if self.ep_square is not None:
            ep_array[self.ep_square] = 1

        aux_planes = [
            bit_array(self.castling_rights),
            ep_array,
            np.full(64, self.turn),
            np.full(64, self.halfmove_clock),
        ]

        game_planes.extend(aux_planes)
        return np.array(game_planes).reshape(8, 8, -1)
