# absearch or negamax search

QS_LIMIT = 219
MATE_VALUE = 30_000
best_move = None

# reaches quiet posiitons from loud positions by running through captures/forced moves


def qs_search(board, score):

    pos = board.copy()

    import eval

    moves = list(pos.legal_moves)

    if len(moves) == 0:
        return -MATE_VALUE

    elif len(moves) == 1:
        copy = pos.copy()
        copy.push(moves[0])

        evl = eval.move(moves[0], pos)

        return -qs_search(copy, -(score + evl))

    else:
        moves = sorted([(eval.move(move, pos), move)
                        for move in moves], key=lambda x: x[0], reverse=True)

        upper = -MATE_VALUE
        best_move = None

        if moves[0][0] < QS_LIMIT:
            return (score)

        for (evl, move) in moves:
            if evl < QS_LIMIT:
                break

            copy = pos.copy()
            copy.push(move)

            curr_search = -qs_search(copy, -(score + evl))
            if curr_search > upper:
                best_move = move
                upper = curr_search

        return (upper)


def search(alpha, beta, pos, depth: int, score: int):

    import chess
    import eval
    from operator import itemgetter

    #################################
    ### Handling of Depth 1 Moves ###
    #################################
    if depth == 0:
        return qs_search(pos, score)

    moves = pos.legal_moves

    if len(moves) == 0:
        return -MATE_VALUE
        
    best_move = None

    for move in pos.moves:
        evl = eval.move(move, pos)
        copy = pos.copy()
        copy.push(move)
        evaluation = -search(-beta, -alpha, copy, depth - 1, -(score + evl))
        if evaluation >= beta:
            return beta
        if evaluation > alpha:
            alpha = score
    return alpha
