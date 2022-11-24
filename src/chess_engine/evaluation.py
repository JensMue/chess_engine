import chess
from numba import jit
import numpy as np

from .utils import make_board_numeric


def request_evaluation(board) -> int:
    """ Request evaluation for numeric board using numba. """
    numeric_board = make_board_numeric(board)
    return compute_evaluation(numeric_board)


@jit(nopython=True)
def compute_evaluation(numeric_board) -> int:
    """ Compute an evaluation for a numeric board with numba. """
    numeric_board[numeric_board==6] = 100
    numeric_board[numeric_board==-6] = -100
    numeric_board[numeric_board==5] = 9
    numeric_board[numeric_board==-5] = -9
    numeric_board[numeric_board==4] = 5
    numeric_board[numeric_board==-4] = -5
    numeric_board[numeric_board==2] = 3
    numeric_board[numeric_board==-2] = -3
    evaluation = np.sum(numeric_board)
    return evaluation


def request_evaluation_nonumba(board) -> int:
    """ Request evaluation for numeric board without numba (for analysis only). """
    numeric_board = make_board_numeric(board)
    return compute_evaluation_nonumba(numeric_board)


def compute_evaluation_nonumba(numeric_board) -> int:
    """ Compute an evaluation for a numeric board without numba (for analysis only). """
    numeric_board[numeric_board==6] = 100
    numeric_board[numeric_board==-6] = -100
    numeric_board[numeric_board==5] = 9
    numeric_board[numeric_board==-5] = -9
    numeric_board[numeric_board==4] = 5
    numeric_board[numeric_board==-4] = -5
    numeric_board[numeric_board==2] = 3
    numeric_board[numeric_board==-2] = -3
    evaluation = np.sum(numeric_board)
    return evaluation
