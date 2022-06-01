import chess
import chess.polyglot
import chess.syzygy
import utils
import random
import numpy as np


class Human:
    """
    A human player decides what moves to make.
    Possible notations are uci ('g1f3') or san ('Nf3').
    """
    def __init__(self, notation='uci'):
        self.notation = notation
        
    def __str__(self):
        return 'Human'
        
    def make_move(self, board):
        while True:
            if self.notation == 'uci':
                options = [i.uci() for i in board.legal_moves]
            elif self.notation == 'san':
                options = [board.san(i) for i in board.legal_moves]
            print(board.unicode())
            print(f'Possible moves: {options}')
            move = str(input("Enter your move (or 'resign'): "))
            if move in options:
                if self.notation == 'uci':
                    return chess.Move.from_uci(move)
                elif self.notation == 'san':
                    return board.parse_san(move)
            elif move == 'resign':
                return 'resign'
            else:
                print('Illegal move. Try again.')
                
                
class SimpleEngine:
    """
    A simple engine that makes moves based on simple heuristics.
    Possible heuristics are 'random', 'attacking', and 'limiting'.
    """
    def __init__(self, heuristic='random'):
        self.heuristic = heuristic
    
    def __str__(self):
        return self.heuristic+'Engine'
    
    def make_move(self, board) -> chess.Move:
        if self.heuristic == 'random':
            return self.random_move(board)
        elif self.heuristic == 'attacking':
            return self.attacking_move(board)
        elif self.heuristic == 'limiting':
            return self.limiting_move(board)
        else:
            raise Exception(f'No heuristic named {self.heuristic} available.')
    
    def random_move(self, board) -> chess.Move:
        return random.choice(list(board.legal_moves))
        
    def attacking_move(self, board) -> chess.Move:
        legal_moves = list(board.legal_moves)
        random.shuffle(legal_moves)
        for move in legal_moves:
            board.push(move)
            if board.is_checkmate(): # test for checkmate
                return board.pop()
            if board.is_check(): # test for check
                return board.pop()
            board.pop()
            if board.is_capture(move): # test for capture
                return move
        return legal_moves[0] # already shuffled
    
    def limiting_move(self, board) -> chess.Move:
        options = {}
        for move in board.legal_moves:
            board.push(move)
            options[move] = -len(list(board.legal_moves))
            board.pop()
        return utils.select_best_move(options)


class NegamaxEngine:
    """
    Chess engine using a negamax algorithm
    with alpha-beta pruning and systematic move-ordering.
    Opening book and endgame tablebase are available.
    """
    def __init__(self, depth=1, opening_book=True, endgame_table=True):
        self.depth = depth
        self.color = None # updated for given board (white=1, black=-1)
        self.opening_book = opening_book
        self.endgame_table = endgame_table
        self.num_evals = 0 # only for statistical purposes
        self.num_prunes = 0 # only for statistical purposes
        
    def __str__(self):
        return f'NegamaxEngineFinal(depth={self.depth})'
    
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
            return (color * utils.evaluate_board(board), None)
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