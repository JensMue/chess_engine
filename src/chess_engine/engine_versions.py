# FILE DESCRIPTION

# This file serves only for documentation and analysis.
# It is not relevant to the rest of the program.

# It contains the following old versions of the final NegamaxEngine:

    # MinimaxEngine:
    #     Chess engine using a plain minimax algorithm without pruning
    
    # NegamaxEngineV1:
    #     Chess engine using a plain negamax algorithm without pruning
    
    # NegamaxEngineV2-4:
    #     Chess engines using a negamax algorithm with pruning.
    #     Moves are either not ordered (V2), randomly ordered (V3) or systematically ordered (V4).
    #     However, in these versions one depth level for pruning is lost.
    #     The reason for that is that negamax is called on the children of the position (improved in V5-7).

    # NegamaxEngineV5-7:
    #     Chess engines using a negamax algorithm with pruning.
    #     Moves are either not ordered (V5), randomly ordered (V6) or systematically ordered (V7).
    #     In these versions the problem from V2-4 is fixed.
    #     This is achieved by calling negamax on the parent node and also returning a move in addition to the evaluation.

    # NegamaxEngineV8:
    #     This version adds an opening book.
    
    # NegamaxEngineV9:
    #     This version adds an endgame tablebase.


# IMPORTS
import chess
import numpy as np

import random

from .evaluation import request_evaluation
from .utils import select_best_move


# PLAIN MINIMAX
class MinimaxEngine:
    """ Chess engine using a plain minimax algorithm without pruning """
    
    def __init__(self, depth=1):
        self.depth = depth
        self.color = None # updated for given board (white=1, black=-1)
        self.num_evals = 0 # only for statistical purposes
    
    def __str__(self):
        return f'MinimaxEngine(depth={self.depth},no_pruning)'
    
    def make_move(self, board) -> chess.Move:    
        self.color = 1 if board.turn else -1
        options = {}
        for move in board.legal_moves:
            board.push(move)
            options[move] = self.color * self.minimax(board, max(self.depth-1,0)) # depth-1 since already depth=1
            board.pop()
        return select_best_move(options)
    
    def minimax(self, board, depth):
        if board.is_game_over(): # check terminal condition
            if board.is_checkmate():
                if board.turn: return float('-Inf')
                else: return float('Inf')
            else: return 0
        if depth == 0: # check depth
            self.num_evals += 1
            return request_evaluation(board)
        if board.turn: #maximizing player (white)
            max_eval = float('-Inf')
            for move in board.legal_moves:
                board.push(move)
                evaluation = self.minimax(board, depth-1)
                max_eval = max(max_eval, evaluation)
                board.pop()
            return max_eval
        else: # minimizing player (black)
            min_eval = float('Inf')
            for move in board.legal_moves:
                board.push(move)
                evaluation = self.minimax(board, depth-1)
                min_eval = min(min_eval, evaluation)
                board.pop()
            return min_eval


# PLAIN NEGAMAX
class NegamaxEngineV1:
    """ Chess engine using a plain negamax algorithm without pruning """
    
    def __init__(self, depth=1):
        self.depth = depth
        self.color = None # updated for given board (white=1, black=-1)
        self.num_evals = 0 # only for statistical purposes
    
    def __str__(self):
        return f'NegamaxEngineV1(depth={self.depth},no_pruning)'
    
    def make_move(self, board) -> chess.Move:
        self.color = 1 if board.turn else -1
        options = {}
        for move in board.legal_moves:
            board.push(move)
            options[move] = -self.negamax(board, -self.color, max(self.depth-1,0)) # depth-1 since already depth=1
            board.pop()
        return select_best_move(options)
    
    def negamax(self, board, color, depth):
        # check terminal conditions
        if board.is_game_over():
            if board.is_checkmate(): return float('-Inf')
            else: return 0 # draw
        if depth == 0:
            self.num_evals += 1
            return color * request_evaluation(board)
        # call negamax recursively as oponent
        max_eval = float('-Inf')
        for move in board.legal_moves:
            board.push(move)
            evaluation = self.negamax(board, -color, depth-1)
            max_eval = max(max_eval, -evaluation)
            board.pop()
        return max_eval


# NEGAMAX AB NO ORDERING - DEPTH-1
class NegamaxEngineV2:
    """ Chess engine using a negamax algorithm with alpha-beta pruning but no move-ordering """
    
    def __init__(self, depth=1):
        self.depth = depth
        self.color = None # updated for given board (white=1, black=-1)
        self.num_evals = 0 # only for statistical purposes
        self.num_prunes = 0 # only for statistical purposes
    
    def __str__(self):
        return f'NegamaxEngineV2(depth={self.depth},ab_depth-1,no_ordering)'
    
    def make_move(self, board) -> chess.Move:
        self.color = 1 if board.turn else -1
        options = {}
        for move in board.legal_moves:
            board.push(move)
            options[move] = -self.negamax(board, -self.color, max(self.depth-1,0), float('-Inf'), float('Inf')) # depth-1 since already depth=1
            board.pop()
        return select_best_move(options)
    
    def negamax(self, board, color, depth, alpha, beta):
        # check terminal conditions
        if board.is_game_over():
            if board.is_checkmate(): return float('-Inf')
            else: return 0 # draw
        if depth == 0:
            self.num_evals += 1
            return color * request_evaluation(board)
        # call negamax recursively as oponent
        max_eval = float('-Inf')
        for move in board.legal_moves:
            board.push(move)
            evaluation = self.negamax(board, -color, depth-1, -beta, -alpha)
            max_eval = max(max_eval, -evaluation)
            board.pop()
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                self.num_prunes += 1
                break
        return max_eval


# NEGAMAX AB RANDOM ORDERING - DEPTH-1
class NegamaxEngineV3:
    """ Chess engine using a negamax algorithm with alpha-beta pruning and random move-ordering"""
    
    def __init__(self, depth=1):
        self.depth = depth
        self.color = None # updated for given board (white=1, black=-1)
        self.num_evals = 0 # only for statistical purposes
        self.num_prunes = 0 # only for statistical purposes
    
    def __str__(self):
        return f'NegamaxEngineV3(depth={self.depth},ab_depth-1,random_ordering)'
    
    def make_move(self, board) -> chess.Move:
        self.color = 1 if board.turn else -1
        options = {}
        for move in board.legal_moves:
            board.push(move)
            options[move] = -self.negamax(board, -self.color, max(self.depth-1,0), float('-Inf'), float('Inf')) # depth-1 since already depth=1
            board.pop()
        return select_best_move(options)
    
    def negamax(self, board, color, depth, alpha, beta):
        # check terminal conditions
        if board.is_game_over():
            if board.is_checkmate(): return float('-Inf')
            else: return 0 # draw
        if depth == 0:
            self.num_evals += 1
            return color * request_evaluation(board)
        # move ordering
        lms = list(board.legal_moves)
        random.shuffle(lms)
        # call negamax recursively as oponent
        max_eval = float('-Inf')
        for move in lms:
            board.push(move)
            evaluation = self.negamax(board, -color, depth-1, -beta, -alpha)
            max_eval = max(max_eval, -evaluation)
            board.pop()
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                self.num_prunes += 1
                break
        return max_eval


# NEGAMAX AB SYSTEMATIC ORDERING - DEPTH-1
class NegamaxEngineV4:
    """ Chess engine using a negamax algorithm with alpha-beta pruning and systematic move-ordering"""
    
    def __init__(self, depth=1):
        self.depth = depth
        self.color = None # updated for given board (white=1, black=-1)
        self.num_evals = 0 # only for statistical purposes
        self.num_prunes = 0 # only for statistical purposes
    
    def __str__(self):
        return f'NegamaxEngineV4(depth={self.depth},ab_depth-1,systematic_ordering)'
    
    def make_move(self, board) -> chess.Move:
        self.color = 1 if board.turn else -1
        options = {}
        for move in board.legal_moves:
            board.push(move)
            options[move] = -self.negamax(board, -self.color, max(self.depth-1,0), float('-Inf'), float('Inf')) # depth-1 since already depth=1
            board.pop()
        return select_best_move(options)
    
    def negamax(self, board, color, depth, alpha, beta):
        # check terminal conditions
        if board.is_game_over():
            if board.is_checkmate(): return float('-Inf')
            else: return 0 # draw
        if depth == 0:
            self.num_evals += 1
            return color * request_evaluation(board)
        # move ordering
        lms = np.array(list(board.legal_moves))
        vals = np.array([0 if board.is_irreversible(lm) else 1 for lm in lms])
        slms = lms[vals.argsort()]
        # call negamax recursively as oponent
        max_eval = float('-Inf')
        for move in slms:
            board.push(move)
            evaluation = self.negamax(board, -color, depth-1, -beta, -alpha)
            max_eval = max(max_eval, -evaluation)
            board.pop()
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                self.num_prunes += 1
                break
        return max_eval


# NEGAMAX AB NO ORDERING
class NegamaxEngineV5:
    """ Chess engine using a plain negamax algorithm with alpha-beta pruning but no move-ordering"""
    
    def __init__(self, depth=1):
        self.depth = depth
        self.color = None # updated for given board (white=1, black=-1)
        self.num_evals = 0 # only for statistical purposes
        self.num_prunes = 0 # only for statistical purposes
        
    def __str__(self):
        return f'NegamaxEngineV5(depth={self.depth},ab_pruning,no_ordering)'
    
    def make_move(self, board) -> chess.Move:
        self.color = 1 if board.turn else -1
        return self.negamax(board, self.color, self.depth, float('-Inf'), float('Inf'))[1]
    
    def negamax(self, board, color, depth, alpha, beta):
        # check terminal conditions
        if board.is_game_over():
            if board.is_checkmate(): return (float('-Inf'), None)
            else: return (0, None) # draw
        if depth == 0:
            self.num_evals += 1
            return (color * request_evaluation(board), None)
        # call negamax recursively as oponent
        max_eval = float('-Inf')
        for move in board.legal_moves:
            board.push(move)
            evaluation = -self.negamax(board, -color, depth-1, -beta, -alpha)[0]
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            board.pop()
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                self.num_prunes += 1
                break   
        return (max_eval, best_move)


# NEGAMAX AB RANDOM ORDERING
class NegamaxEngineV6:
    """ Chess engine using a plain negamax algorithm with alpha-beta pruning and random move-ordering"""
    
    def __init__(self, depth=1):
        self.depth = depth
        self.color = None # updated for given board (white=1, black=-1)
        self.num_evals = 0 # only for statistical purposes
        self.num_prunes = 0 # only for statistical purposes
        
    def __str__(self):
        return f'NegamaxEngineV6(depth={self.depth},ab_pruning,random_ordering)'
    
    def make_move(self, board) -> chess.Move:
        self.color = 1 if board.turn else -1
        return self.negamax(board, self.color, self.depth, float('-Inf'), float('Inf'))[1]
    
    def negamax(self, board, color, depth, alpha, beta):
        # check terminal conditions
        if board.is_game_over():
            if board.is_checkmate(): return (float('-Inf'), None)
            else: return (0, None) # draw
        if depth == 0:
            self.num_evals += 1
            return (color * request_evaluation(board), None)
        # move ordering
        lms = list(board.legal_moves)
        random.shuffle(lms)
        # call negamax recursively as oponent
        max_eval = float('-Inf')
        for move in lms:
            board.push(move)
            evaluation = -self.negamax(board, -color, depth-1, -beta, -alpha)[0]
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            board.pop()
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                self.num_prunes += 1
                break   
        return (max_eval, best_move)


# NEGAMAX AB SYSTEMATIC ORDERING
class NegamaxEngineV7:
    """ Chess engine using a plain negamax algorithm with alpha-beta pruning and systematic move-ordering"""
    
    def __init__(self, depth=1):
        self.depth = depth
        self.color = None # updated for given board (white=1, black=-1)
        self.num_evals = 0 # only for statistical purposes
        self.num_prunes = 0 # only for statistical purposes
        
    def __str__(self):
        return f'NegamaxEngineV7(depth={self.depth},ab_pruning,systematic_ordering)'
    
    def make_move(self, board) -> chess.Move:
        self.color = 1 if board.turn else -1
        return self.negamax(board, self.color, self.depth, float('-Inf'), float('Inf'))[1]
    
    def negamax(self, board, color, depth, alpha, beta):
        # check terminal conditions
        if board.is_game_over():
            if board.is_checkmate(): return (float('-Inf'), None)
            else: return (0, None) # draw
        if depth == 0:
            self.num_evals += 1
            return (color * request_evaluation(board), None)
        # systematic move ordering
        lms = np.array(list(board.legal_moves))
        vals = np.array([0 if board.is_capture(lm) else 1 for lm in lms])
        slms = lms[vals.argsort()]
        # call negamax recursively as oponent
        best_move = None
        max_eval = float('-Inf')
        for move in slms:
            board.push(move)
            evaluation = -self.negamax(board, -color, depth-1, -beta, -alpha)[0]
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            board.pop()
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                self.num_prunes += 1
                break   
        return (max_eval, best_move)


# NEGAMAX AB SYSTEMATIC ORDERING + OPENING BOOK
class NegamaxEngineV8:
    """
    Chess engine using a plain negamax algorithm
    with alpha-beta pruning and systematic move-ordering.
    Opening book available
    """
    def __init__(self, depth=1, opening_book=True):
        self.depth = depth
        self.color = None # updated for given board (white=1, black=-1)
        self.opening_book = opening_book
        self.num_evals = 0 # only for statistical purposes
        self.num_prunes = 0 # only for statistical purposes
        
    def __str__(self):
        return f'NegamaxEngineV8(depth={self.depth},ab,so,ob)'
    
    def make_move(self, board) -> chess.Move:
        if self.opening_book: # check opening book
                try:
                    with chess.polyglot.open_reader("polyglot/performance.bin") as reader:
                        return reader.weighted_choice(board).move
                except:
                    self.opening_book = False
        self.color = 1 if board.turn else -1
        return self.negamax(board, self.color, self.depth, float('-Inf'), float('Inf'))[1]
    
    def negamax(self, board, color, depth, alpha, beta):
        # check terminal conditions
        if board.is_game_over():
            if board.is_checkmate(): return (float('-Inf'), None)
            else: return (0, None) # draw
        if depth == 0:
            self.num_evals += 1
            return (color * request_evaluation(board), None)
        # systematic move ordering
        lms = np.array(list(board.legal_moves))
        vals = np.array([0 if board.is_capture(lm) else 1 for lm in lms])
        slms = lms[vals.argsort()]
        # call negamax recursively as oponent
        best_move=None
        max_eval = float('-Inf')
        for move in slms:
            board.push(move)
            evaluation = -self.negamax(board, -color, depth-1, -beta, -alpha)[0]
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            board.pop()
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                self.num_prunes += 1
                break   
        return (max_eval, best_move)
    
    
# NEGAMAX AB SYSTEMATIC ORDERING + ENDGAME TABLEBASE
class NegamaxEngineV9:
    """
    Chess engine using a plain negamax algorithm
    with alpha-beta pruning and systematic move-ordering.
    Opening book and endgame tablebase available
    """
    def __init__(self, depth=1, opening_book=True, endgame_table=True):
        self.depth = depth
        self.color = None # updated for given board (white=1, black=-1)
        self.opening_book = opening_book
        self.endgame_table = endgame_table
        self.num_evals = 0 # only for statistical purposes
        self.num_prunes = 0 # only for statistical purposes
        
    def __str__(self):
        return f'NegamaxEngineV9(depth={self.depth},ab,so,ob,et)'
    
    def make_move(self, board) -> chess.Move:
        if self.opening_book: # check opening book
                try:
                    with chess.polyglot.open_reader("polyglot/performance.bin") as reader:
                        return reader.weighted_choice(board).move
                except:
                    self.opening_book = False
        self.color = 1 if board.turn else -1
        return self.negamax(board, self.color, self.depth, float('-Inf'), float('Inf'))[1]
    
    def negamax(self, board, color, depth, alpha, beta):
        # check terminal conditions
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
        # systematic move ordering
        lms = np.array(list(board.legal_moves))
        vals = np.array([0 if board.is_capture(lm) else 1 for lm in lms])
        slms = lms[vals.argsort()]
        # call negamax recursively as oponent
        best_move=None
        max_eval = float('-Inf')
        for move in slms:
            board.push(move)
            evaluation = -self.negamax(board, -color, depth-1, -beta, -alpha)[0]
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            board.pop()
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                self.num_prunes += 1
                break   
        return (max_eval, best_move)