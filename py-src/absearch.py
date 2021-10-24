# absearch or negamax search

import evaluate

QS_LIMIT = 219
MATE_VALUE = 30_000
best_move = None

# reaches quiet posiitons from loud positions by running through captures/forced moves
def get_moves(pos, depth):

    depth = max(depth, 0)

    for move in pos.legal_moves:
        
        if depth > 0 or (pos.is_capture(move) and pos.piece_type_at(move.to_square) != 1):
            yield move  



class Searcher:
    def __init__(self):
        self.tp_score = {}
        self.tp_move = {}
        self.history = set()
        self.nodes = 0

def queiesce(alpha, beta, pos):
    moves = list(get_moves(pos,0))

    stand_pat = -evaluate.position(pos)

    if len(moves) == 0: return stand_pat

    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    for move in moves:

        pos.push(move)
        score = -queiesce(-beta, -alpha, pos)
        pos.pop()

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
        
    return alpha

def alpha_beta(alpha, beta, depth, pos):

    if depth == 0: return (queiesce(alpha, beta, pos), None)

    if pos.outcome() is not None:
        return (queiesce(alpha, beta, pos), None)

    moves = get_moves(pos, depth)
    best_move = None
    for move in moves:
        pos.push(move)
        score = -alpha_beta(-beta, -alpha, depth-1, pos)[0]
        pos.pop()

        if (score >= beta):
            return (beta, None)
        if score > alpha:
            alpha = score
            best_move = move
    return (alpha, best_move)