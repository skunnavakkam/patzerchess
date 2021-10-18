def main():

    import chess
    import eval
    import random
    from absearch import search, qs_search
    from operator import itemgetter

    board = chess.Board(
        fen="r1bqkbnr/ppp2ppp/2np4/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 4")

    moves = sorted([(eval.move(move, pos), move)
                    for move in moves], key=lambda x: x[0], reverse=True)


if __name__ == "__main__":
    main()
