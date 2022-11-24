import chess
import chess.pgn

from .utils import find_stoppage_reason


def game(player_white, player_black, verbose=True) -> chess.Board:
    """ Play a single game of chess. """
    
    # Instantiate board
    board=chess.Board()
    
    # Play game
    while not board.is_game_over(claim_draw=True):
        # White to move
        if board.turn:
            move = player_white.make_move(board)
        # Black to move
        else:
            move = player_black.make_move(board)
        # Check for resignation
        if move == 'resign': return board
        # Print game progress information
        if verbose:
            side = 'White' if board.turn else 'Black'
            print(f'Move {board.fullmove_number}, {side} plays {move}.')
        # Make the selected move
        board.push(move)
    
    return board


def match(player_white, player_black, num_games=1, verbose=True) -> dict:
    """
    Play a match of chess between two players.
    The number of games in the match can be specified.
    One player has the white pieces in all games.
    """
    
    # Create placeholder for match results
    match_result = {
        'player_white': str(player_white),
        'player_black': str(player_black), 
        'num_games': num_games, 
        'num_moves': 0, 
        'results': {'1-0': 0, '1/2-1/2': 0, '0-1': 0, '*': 0}, 
        'endings': {
            'checkmate': 0, 
            'stalemate': 0, 
            'insuff_mat': 0, 
            'fifty_moves': 0, 
            'threefold_rep': 0, 
            'resign': 0
            }, 
        'PGNs': []
        }
    
    # Play games
    for i in range(num_games):
        current_game = game(player_white, player_black, verbose=False)
        result = current_game.result(claim_draw=True)
        ending = find_stoppage_reason(current_game)
        # Save results in dictionary
        match_result['num_moves'] += current_game.fullmove_number
        match_result['results'][result] += 1
        match_result['endings'][ending] +=1
        match_result['PGNs'].append(chess.pgn.Game.from_board(current_game))
        # Print match progress updates
        if verbose:
            print(f'Game {i+1}: {result}, {current_game.fullmove_number} moves, {ending}')
    
    return match_result


def tournament(players_list, num_games=1, verbose=True) -> dict:
    """
    Play a tournament between specified players.
    Each two players play two matches against another so each one has the white pieces once.
    The number of games per match can be specified.
    """
    
    # Setup placeholder for tournament results
    tournament_result = []
    white_results = {str(k):[0,0,0,0] for k in players_list}
    black_results = {str(k):[0,0,0,0] for k in players_list}
    total_results = {str(k):[0,0,0,0] for k in players_list}
    
    # Let each player play a match against all other players
    for player_white in players_list:
        for player_black in players_list:
            # Start a match
            #print(f'\nNew Match: {str(player_white)} vs {str(player_black)}')
            match_result = match(player_white, player_black, num_games, verbose=False)
            mr = list(match_result['results'].values())
            print(f'Match: {str(player_white)} vs {str(player_black)}: {mr}')
            # Append match results to tournament results
            tournament_result.append(match_result)
            for i in range(4):
                white_results[str(player_white)][i] += mr[i]
                black_results[str(player_black)][i] += mr[i]
                
    # Combine white and black results for each player
    for k in total_results.keys():
        total_results[k][0] = white_results[k][0] + black_results[k][2]
        total_results[k][1] = white_results[k][1] + black_results[k][1]
        total_results[k][2] = white_results[k][2] + black_results[k][0]
        total_results[k][3] = white_results[k][3] + black_results[k][3]
    
    # Print tournament results
    print('white_results',white_results)
    print('black_results',black_results)
    print('total_results',total_results)
    
    # Return detailed outcomes of all games or summarized results
    # return tournament_result 
    return total_results
