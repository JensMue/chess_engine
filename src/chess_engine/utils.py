import chess
import numpy as np

import random


def find_stoppage_reason(board) -> str:
    """ Find reason for game stoppage. """
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
    

def make_board_numeric(board) -> np.array:
    """ Convert the board object to a Numpy array for fast evaluation. """
    numeric_board = np.zeros(64)
    # Add white pieces
    for sq in chess.scan_reversed(board.occupied_co[chess.WHITE]):
        numeric_board[sq] = board.piece_type_at(sq)
    # Add black pieces
    for sq in chess.scan_reversed(board.occupied_co[chess.BLACK]):
        numeric_board[sq] = -board.piece_type_at(sq)
    return numeric_board
    

def select_best_move(options) -> chess.Move:
    """ Select best move from list of moves and evaluations. """
    # Find the maximum move evaluation.
    best_score = max(options.values())
    # Filter all moves with the maximum evaluation.
    best_options = [k for (k, v) in options.items() if v == best_score]
    # Select a random move with the maximum evaluation
    return random.choice(best_options)
