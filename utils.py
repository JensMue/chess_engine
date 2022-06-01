import chess
import numpy as np
import random
from numba import jit

# FIND CHECK GAME END REASON
def find_ending(board) -> str:
    if board.is_checkmate():
        return 'checkmate'
    elif board.is_stalemate():
        return 'stalemate'
    elif board.is_insufficient_material():
        return 'insuff_mat'
    elif board.can_claim_fifty_moves():
        return 'fifty_moves'
    elif board.can_claim_threefold_repetition():
        return 'threefold_rep'
    else:
        return 'resign'
    
# SELECT BEST MOVE
def select_best_move(options) -> chess.Move:
    best_score = max(options.values())
    best_options = [k for (k, v) in options.items() if v == best_score]
    return random.choice(best_options)

# STATIC EVALUATION OF BOARD
def evaluate_board(board) -> int:
    numeric_board = convert_to_numeric(board)
    return compute_evaluation(numeric_board)

# STATIC EVALUATION OF BOARD WITHOUT NUMBA
def evaluate_board_nonumba(board) -> int:
    numeric_board = convert_to_numeric(board)
    return compute_evaluation_nonumba(numeric_board)

# CONVERT BOARD TO NUMERIC
def convert_to_numeric(board):
    numeric_board = np.zeros(64)
    for sq in chess.scan_reversed(board.occupied_co[chess.WHITE]):  # Check if white
        numeric_board[sq] = board.piece_type_at(sq)
    for sq in chess.scan_reversed(board.occupied_co[chess.BLACK]):  # Check if black
        numeric_board[sq] = -board.piece_type_at(sq)
    return numeric_board

# COMPUTE EVALUATION WITH NUMBA
@jit(nopython=True)
def compute_evaluation(numeric_board):
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

# COMPUTE EVALUATION WITHOUT NUMBA
def compute_evaluation_nonumba(numeric_board):
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






