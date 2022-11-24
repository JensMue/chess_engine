#!/usr/bin/env python3

from src.chess_engine import setup_game
from src.chess_engine import game


# Confirm program execution
print("\nWelcome!\n{0}\n{1}".format(
    '1: Play chess', 
    '2: Quit program'))
choice = str(input())

# Start program
if choice == '1':
    
    # Game setup
    print("\n{0}\n{1}\n{2}".format(
    '----------', 
    'Game setup', 
    '----------'))
    player_white, player_black = setup_game()

    # Play game
    print("\n{0}\n{1}\n{2}".format(
    '----------', 
    'Game start', 
    '----------'))
    game_result = game(player_white, player_black)
    print(game_result)
    print('\nThank you for playing!')

# Exit program
elif choice != '1':
    print('\nBye!')
