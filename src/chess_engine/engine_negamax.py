import chess
import chess.polyglot
import chess.syzygy
import numpy as np

from .evaluation import request_evaluation


class NegamaxEngine:
    """
    Chess engine using a negamax algorithm.
    Includes alpha-beta pruning and systematic move-ordering.
    Opening book and endgame tablebase are available.
    """
    
    def __init__(self, depth=1, opening_book=True, endgame_table=True):
        self.depth = int(depth)
        self.color = None # updated for given board (white=1, black=-1)
        self.opening_book = opening_book
        self.endgame_table = endgame_table
        self.num_evals = 0 # only for statistical purposes
        self.num_prunes = 0 # only for statistical purposes
        
    def __str__(self):
        return f'NegamaxEngine(depth={self.depth})'
    
    def make_move(self, board) -> chess.Move:
        # Check opening book
        if self.opening_book: 
                try:
                    with chess.polyglot.open_reader("polyglot/performance.bin") as reader:
                        return reader.weighted_choice(board).move
                except:
                    self.opening_book = False
        # Determine color
        self.color = 1 if board.turn else -1
        # Call negamax search algorithm
        return self.negamax(board, self.color, self.depth, float('-Inf'), float('Inf'))[1]
    
    def negamax(self, board, color, depth, alpha, beta):
        """ Negamax search algorithm recursively calling the evaluation function. """
        
        # Check conditions to exit recursion
        if board.is_game_over():
            if board.is_checkmate(): return (float('-Inf'), None)
            else: return (0, None) # draw
        if depth == 0:
            if self.endgame_table: # check endgame table
                try:
                    with chess.gaviota.open_tablebase("syzygy") as tablebase:
                        wdl = tablebase.probe_wdl(board)
                        return wdl * 100
                except:
                    pass
            self.num_evals += 1
            return (color * request_evaluation(board), None)
        
        # Systematic move ordering
        move_options = np.array(list(board.legal_moves))
        priorities = np.array([0 if board.is_capture(move_option) else 1 for move_option in move_options])
        sorted_move_options = move_options[priorities.argsort()]
        
        # Set temporary optimum move and evaluation (random move to avoid NA error before checkmate)
        best_move=sorted_move_options[0] 
        max_eval = float('-Inf')
        
        # Loop through sorted move options
        for move in sorted_move_options:
            board.push(move)
            # Call negamax recursively as oponent
            evaluation = -self.negamax(board, -color, depth-1, -beta, -alpha)[0]
            # Test for new best move and evaluation
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            board.pop()
            # Pruning
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                self.num_prunes += 1
                break   
        
        # Return move with highest evaluation
        return (max_eval, best_move)
