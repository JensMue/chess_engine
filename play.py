# PLAY GAME

import games
import players

want_play = str(input('Welcome! Do you want to play a game of chess? (y/n)'))

if want_play == 'n':
    print('Bye')

if want_play == 'y':
    
    opponent = str(input('Who do you want to play against? (RandomEngine/AttackingEngine/LimitingEngine/NegamaxEngine)'))

    if opponent == 'RandomEngine':
        engine = players.SimpleEngine('random')
    elif opponent == 'AttackingEngine':
        engine = players.SimpleEngine('attacking')
    elif opponent == 'LimitingEngine':
        engine = players.SimpleEngine('limiting')
    elif opponent == 'NegamaxEngine':
        depth = str(input('What depth do you want? (recommended: 5)'))
        engine = players.NegamaxEngine(depth=depth)
    else:
        raise Exception('No such player available')
        
    side = str(input('Do you want to play as white or black? (w/b)'))
    notation = str(input('Which notation do you want? (san/uci)'))
    
    if side == 'w':
        player_white = players.Human(notation=notation)
        player_black = engine
    elif side == 'b':
        player_white = engine
        player_black = players.Human(notation=notation)
        
    # play game
    game_result = games.game(player_white, player_black)
    print(game_result)
    print('Thank you for playing!')