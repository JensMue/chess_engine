import chess

import random

from .utils import select_best_move


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
        """ Make a random legal move. """
        return random.choice(list(board.legal_moves))
        
    def attacking_move(self, board) -> chess.Move:
        """ Make a legal attacking move (checkmate > check > capture). """
        legal_moves = list(board.legal_moves)
        random.shuffle(legal_moves)
        for move in legal_moves:
            board.push(move)
            # Test for checkmate
            if board.is_checkmate(): 
                return board.pop()
            # Test for check
            if board.is_check(): 
                return board.pop()
            board.pop()
            # Test for capture
            if board.is_capture(move): 
                return move
        return legal_moves[0] # already shuffled
    
    def limiting_move(self, board) -> chess.Move:
        """ Make a move that limits opponents number of legal move. """
        options = {}
        for move in board.legal_moves:
            board.push(move)
            options[move] = -len(list(board.legal_moves))
            board.pop()
        return select_best_move(options)
