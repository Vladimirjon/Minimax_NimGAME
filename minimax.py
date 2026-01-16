"""
Minimax Algorithm with Alpha-Beta Pruning
For playing Nim optimally.
"""

import copy

def minimax(game, alpha=float('-inf'), beta=float('inf'), maximizing=True):
    """
    Implements the minimax algorithm with alpha-beta pruning.
    
    Args:
        game: Current game state (Nim object)
        alpha: Alpha value for pruning
        beta: Beta value for pruning
        maximizing: True if maximizing player, False if minimizing
        
    Returns:
        Tuple (best_value, best_action)
    """
    # Base case: terminal state
    if game.is_terminal():
        winner = game.winner()
        if winner == game.player:
            return (1, None)  # Current player won
        else:
            return (-1, None)  # Current player lost
    
    best_action = None
    
    if maximizing:
        best_value = float('-inf')
        for action in game.available_actions():
            # Make a copy of the game to try this action
            game_copy = copy.deepcopy(game)
            game_copy.move(action)
            
            # Recursively evaluate this action
            value, _ = minimax(game_copy, alpha, beta, False)
            
            if value > best_value:
                best_value = value
                best_action = action
            
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break  # Beta cutoff
    else:
        best_value = float('inf')
        for action in game.available_actions():
            # Make a copy of the game to try this action
            game_copy = copy.deepcopy(game)
            game_copy.move(action)
            
            # Recursively evaluate this action
            value, _ = minimax(game_copy, alpha, beta, True)
            
            if value < best_value:
                best_value = value
                best_action = action
            
            beta = min(beta, best_value)
            if beta <= alpha:
                break  # Alpha cutoff
    
    return (best_value, best_action)

def get_best_move(game):
    """
    Returns the best move for the current player using minimax.
    
    Args:
        game: Current game state (Nim object)
        
    Returns:
        Best action (pile, count) tuple
    """
    _, best_action = minimax(game, maximizing=True)
    return best_action
