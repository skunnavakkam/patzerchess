
from game import Board
import numpy

# these are for typecheckers

def Value(position: Board) -> float:
    return 0.0

def Policy(position: Board):
    return None

def EndgameValue(position: Board) -> float:
    return 0.0

def EndgamePolicy(position: Board): 
    return None