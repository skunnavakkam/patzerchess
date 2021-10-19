# absearch or negamax search

import eval

QS_LIMIT = 219
MATE_VALUE = 30_000
best_move = None

# reaches quiet posiitons from loud positions by running through captures/forced moves


def get_moves(pos, depth):

    depth = max(depth, 0)

    def dummy_eval(move):
        return eval.move(move, pos)

    mvs = sorted(pos.legal_moves, key=dummy_eval, reverse=True)

    for move in mvs:
        evl = eval.move(move, pos)
        if depth > 0 or evl > QS_LIMIT:
            yield move


class Searcher:
    def __init__(self):
        self.tp_score = {}
        self.tp_move = {}
        self.history = set()
        self.nodes = 0


def search(alpha, beta, pos, depth: int, score: int):

    import chess
    import eval
    from operator import itemgetter

    if depth == 0:
        moves = get_moves(pos, depth)
        if moves.count() == 0:
            return -score
        else:
            copy = pos.copy()
            copy.push(move)
            return (-beta, -alpha, copy, depth - 1, )

    else:
