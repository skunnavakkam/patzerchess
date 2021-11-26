
import chess
import chess.svg
import numpy as np

def bitboard_to_svg(bitboard):
    squares = chess.SquareSet(bitboard)
    chess.svg.board(None, squares=squares)
