# absearch or negamax search

import evaluate
import chess
import chess.polyglot

TABLE_SIZE = 1E7
MATE_VALUE = 524_288

class ABSearcher:
    
    def __init__(self):
        # Basically handles transpositions
        # TRANS TABLE FORMAT:
        # {(zobrist): ((score, move), depth)}
        # The reason we have a seperate depth tag is to facilitate the following:
        # Understandably, the greater the search depth the better the evaluation
        # Thus, by adding in a depth tag, we are able to pick positions with max depth
        # In addition, if we search a position to a greater depth, we are able to replace the dict Entry
        # this would maximise both the depth of the entries in the dictionary and the depth of the vals we pull
        self.tp = {}
        self.nodes = 0

    # Our overarching Alpha-Beta search. I plan to wrap this in an iterative deepening framework
    # Using transpositions as Trans
    def alpha_beta(self, alpha, beta, depth, pos):

        zobrist = chess.polyglot.zobrist_hash(pos)
        trans = self.tp.get(zobrist)
        if trans is not None:
            ((trans_score, trans_move), trans_depth) = trans
            if trans_depth >= depth:
                return (trans_score, trans_move)
        # now can guarantee that the all moves generated need to be appended to the dictionary
        # This is due to that it doesn't exist 

        if depth == 0: return (self.queiesce(alpha, beta, pos), None)

        if pos.outcome() is not None:
            return (self.queiesce(alpha, beta, pos), None)

        moves = self.get_moves(pos, depth)
        best_move = None
        for move in moves:
            pos.push(move)
            score = -self.alpha_beta(-beta, -alpha, depth-1, pos)[0]
            pos.pop()

            if (score >= beta):
                self.tp[zobrist] = ((beta, None), depth)
                return (beta, None)
            if score > alpha:
                alpha = score
                best_move = move
        
        self.tp[zobrist] = ((alpha, best_move), depth)
        return (alpha, best_move)


    ##### QUEIESCE SEARCH #####
    # Reaches calm positions from positions with captures
    # is important, since it basically blunder checks
    def queiesce(self, alpha, beta, pos):

        zobrist = chess.polyglot.zobrist_hash(pos)
        trans = self.tp.get(zobrist)
        if trans is not None:
            ((trans_score, trans_move), trans_depth) = trans
            return trans_score

        moves = list(self.get_moves(pos,0))

        stand_pat = -evaluate.position(pos)

        if len(moves) == 0: 
            self.tp[zobrist] = ((stand_pat, None), 0)
            return stand_pat

        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        for move in moves:

            pos.push(move)
            score = -self.queiesce(-beta, -alpha, pos)
            pos.pop()

            if score >= beta:
                self.tp[zobrist] = ((beta, None), 0)
                return beta
            if score > alpha:
                alpha = score
        
        self.tp[zobrist] = ((alpha, None), 0)
        return alpha

    # reaches quiet posiitons from loud positions by running through captures/forced moves
    def get_moves(self, pos, depth):

        depth = max(depth, 0)

        for move in pos.legal_moves:
            
            if depth > 0 or (pos.is_capture(move) and pos.piece_type_at(move.to_square) != 1):
                yield move


    ##### SEARCH #####
    # Returns a generator object, based on iterative deepening.
    # Returns a tuple of (move, score, depth)
    # again a lot of code taken from sunfish
    def search(self, pos):

        alpha = -MATE_VALUE
        beta = MATE_VALUE

        # loop of finite length for two reasons:
        # for loops are faster than while loops AND
        # we don't want people searching to depth infin lest there might be a trans table overflow

        self.tp.clear()

        for depth in range(1,1000):
            yield self.alpha_beta(alpha, beta, depth, pos)

        # you would almost never reach here
        print("You, you have been here a long time")

