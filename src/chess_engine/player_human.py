import chess


class HumanPlayer:
    """
    A human player decides what moves to make.
    Possible notations are uci san ('Nf3') or ('g1f3').
    """
    
    def __init__(self, side='white', notation='uci', visualization='str', theme='dark'):
        orientations = {'white': True, 'black': False}
        self.orientation = orientations[side]
        self.notation = notation
        self.visualization = visualization
        if theme:
            color_reversals = {'dark': True, 'light': False}
            self.invert_color = color_reversals[theme]
        
    def __str__(self):
        return 'HumanPlayer'
        
    def make_move(self, board):
        while True:
            
            # Compute move options
            if self.notation == 'uci':
                options = [i.uci() for i in board.legal_moves]
            elif self.notation == 'san':
                options = [board.san(i) for i in board.legal_moves]
            
            # Print board visualization and move options
            print('')
            if self.visualization == 'str':
                print(board)
            elif self.visualization == 'unicode':
                print(board.unicode(invert_color=self.invert_color, orientation=self.orientation))
            print(f'\nPossible moves: {options}')
            
            # Make move
            move = str(input("Enter your move (or 'resign' to exit): "))
            
            # Check move legality
            if move in options:
                if self.notation == 'uci':
                    return chess.Move.from_uci(move)
                elif self.notation == 'san':
                    return board.parse_san(move)
            elif move == 'resign':
                return 'resign'
            else:
                print('Illegal move. Try again.')
