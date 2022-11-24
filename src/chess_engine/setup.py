import chess

from .engine_negamax import NegamaxEngine
from .engine_simple import SimpleEngine
from .player_human import HumanPlayer


def setup_game():
    """ 
    Configure game settings (engine, color, visualization). 
    Returns: Two player instances (as white and black)
    """
    
    # Get user configurations
    engine = select_engine()
    color = select_color()
    notation = select_notation()
    visualization, theme = select_visualization()
    
    
    # Instantiate human player
    human = HumanPlayer(side=color, 
        notation=notation, 
        visualization=visualization, 
        theme=theme
        )
    
    # Return players
    if color == 'white':
        return human, engine
    elif color == 'black':
        return engine, human
    
    
def select_engine():
    """ 
    Select the type of chess engine to play against. 
    Returns: instance of engine class
    """
    
    # Show options and get user input
    print("\nSelect engine:\n{0}\n{1}\n{2}\n{3}".format(
        '1: RandomEngine (plays random legal moves)', 
        '2: AttackingEngine (plays attacking moves)',
        '3: LimitingEngine (limits your legal moves)',
        '4: NegamaxEngine (STRONGEST, evaluates at user-specified depth)'))
    choice = str(input())
    
    # RandomEngine
    if choice == '1': 
        print('RandomEngine selected')
        return SimpleEngine('random')
    
    # AttackingEngine
    elif choice == '2':
        print('AttackingEngine selected')
        return SimpleEngine('attacking')
        
    # LimitingEngine
    elif choice == '3':
        print('LimitingEngine selected.')
        return SimpleEngine('limiting')
        
    # NegamaxEngine
    elif choice == '4':
        print("\nSelect engine depth:\n{0}\n{1}".format(
            'Higher depth -> stronger play, but slower evaluation', 
            'Recommended: 5'))
        depth = str(input())
        print(f'NegamaxEngine selected (depth = {depth})')
        return NegamaxEngine(depth=depth)
      
    # Invalid entry
    else:
        raise Exception('No valid engine selected.')
    

def select_color() -> str:
    """ Let user select which color to play as. """
    
    # Show options
    print("\nSelect color:\n{0}\n{1}".format(
        '1: White', 
        '2: Black'))
    
    # Get user input
    choice = str(input())
    if choice == '1':
        return 'white'
    elif choice == '2':
        return 'black'
    else:
        raise Exception('No valid color selected.')


def select_notation() -> str:
    """ Let user select a chess notation method. """
    
    # Show options
    print("\nSelect notation:\n{0}\n{1}".format(
        "1: SAN - Standard algebraic notation by FIDE (e.g. 'Nf3')", 
        "2: UCI - Universal chess interface (e.g. 'g1f3')"))
    
    # Get user input
    choice = str(input())
    if choice == '1':
        return 'san'
    elif choice == '2':
        return 'uci'
    else:
        raise Exception('No valid notation selected.')


def select_visualization() -> tuple:
    """ Let user select a board visualization method. """
    
    # Print unicode board
    print('')
    print(chess.Board().unicode())
    print('')

    # Show options and get user input
    print("Select board visualization:\n{0}\n{1}\n{2}\n{3}\n{4}".format(
        "Some terminals do not show unicode symbols.", 
        "If you can see the chess pieces above this prompt, select option 1.",
        "Otherwise, select 2 to use strings or try another interface (e.g. Visual Studio Code).",
        "1: Unicode representation", 
        "2: String representation"))
    choice = str(input())
    
    # Unicode board representation
    if choice == '1': 
        visualization = 'unicode'
        # Select theme
        print("\nSelect your editor theme (for correct piece coloring):\n{0}\n{1}".format(
            '1: Dark', 
            '2: Light'))
        user_theme = str(input())
        if user_theme == '1':
            return visualization, 'dark'
        else:
            return visualization, 'light'
    elif choice == '2': # string board representation
        visualization = 'str'
        return visualization, None # theme not relevant for string representation
    else: # invalid input
        raise Exception('No valid visualization selected.')
