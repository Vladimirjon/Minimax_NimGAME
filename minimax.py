"""
Minimax Algorithm with Alpha-Beta Pruning
For playing Nim optimally.
"""

import copy

def minimax(game, maximizing_player, alpha=float('-inf'), beta=float('inf')):
    """
    Implements the minimax algorithm with alpha-beta pruning.
    
    Args:
        game: Current game state (Nim object)
        maximizing_player: The player we're trying to maximize for (0 or 1)
        alpha: Alpha value for pruning
        beta: Beta value for pruning
        
    Returns:
        Tuple (best_value, best_action)
    """
    # Base case: terminal state
    if game.is_terminal():
        winner = game.winner()
        if winner == maximizing_player:
            return (1, None)  # Maximizing player won
        else:
            return (-1, None)  # Maximizing player lost
    
    best_action = None
    
    # Check if it's the maximizing player's turn
    if game.player == maximizing_player:
        # Maximizing
        best_value = float('-inf')
        for action in game.available_actions():
            # Make a copy of the game to try this action
            game_copy = copy.deepcopy(game)
            game_copy.move(action)
            
            # Recursively evaluate this action
            value, _ = minimax(game_copy, maximizing_player, alpha, beta)
            
            if value > best_value:
                best_value = value
                best_action = action
            
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break  # Beta cutoff
    else:
        # Minimizing
        best_value = float('inf')
        for action in game.available_actions():
            # Make a copy of the game to try this action
            game_copy = copy.deepcopy(game)
            game_copy.move(action)
            
            # Recursively evaluate this action
            value, _ = minimax(game_copy, maximizing_player, alpha, beta)
            
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
    _, best_action = minimax(game, game.player)
    return best_action
