"""
minimax.py - Minimax Algorithm Implementation

This module implements the Minimax decision algorithm with memoization
for the Nim game. The algorithm finds the optimal action for any game state.

Key concepts:
- MAX player tries to maximize the utility (wants to win)
- MIN player tries to minimize the utility (wants MAX to lose)
- Memoization caches results for (N_remaining, player) pairs
"""

import time
from typing import Tuple, Dict, Optional


class MinimaxStats:
    """
    Tracks statistics for a single minimax decision.
    
    Attributes:
        nodes_evaluated: Number of game states evaluated
        max_depth_reached: Maximum depth of the search tree explored
        elapsed_time_ms: Time taken to make the decision in milliseconds
    """
    
    def __init__(self):
        self.nodes_evaluated = 0
        self.max_depth_reached = 0
        self.elapsed_time_ms = 0.0
    
    def __repr__(self) -> str:
        return (f"MinimaxStats(nodes={self.nodes_evaluated}, "
                f"depth={self.max_depth_reached}, time={self.elapsed_time_ms:.2f}ms)")


# Global memoization cache: (n_remaining, player_to_move) -> (best_action, value)
_memo_cache: Dict[Tuple[int, int], Tuple[Optional[int], int]] = {}


def clear_memo_cache():
    """Clear the memoization cache."""
    global _memo_cache
    _memo_cache.clear()


def get_memo_cache_size() -> int:
    """Return the current size of the memoization cache."""
    return len(_memo_cache)


def minimax(game_state, max_player: int = 0) -> Tuple[Optional[int], int, MinimaxStats]:
    """
    Compute the best action and its value using the Minimax algorithm.
    
    This is the main entry point for minimax decisions. It wraps the
    recursive _minimax_value function and collects statistics.
    
    Args:
        game_state: A NimGame instance representing the current state
        max_player: The player designated as MAX (default: 0)
        
    Returns:
        Tuple of (best_action, value, stats) where:
        - best_action: The optimal action to take (1, 2, or 3), or None if terminal
        - value: The minimax value of the state (+1 for MAX win, -1 for MAX loss)
        - stats: MinimaxStats instance with performance metrics
    """
    stats = MinimaxStats()
    start_time = time.perf_counter()
    
    # Call the recursive minimax with memoization
    best_action, value = _minimax_value(
        n_remaining=game_state.n_remaining,
        current_player=game_state.current_player,
        max_player=max_player,
        depth=0,
        stats=stats
    )
    
    end_time = time.perf_counter()
    stats.elapsed_time_ms = (end_time - start_time) * 1000
    
    return best_action, value, stats


def _minimax_value(n_remaining: int, current_player: int, max_player: int,
                   depth: int, stats: MinimaxStats) -> Tuple[Optional[int], int]:
    """
    Recursive minimax with memoization.
    
    Args:
        n_remaining: Number of sticks remaining
        current_player: Player whose turn it is (0 or 1)
        max_player: The player designated as MAX
        depth: Current depth in the search tree
        stats: MinimaxStats instance to update
        
    Returns:
        Tuple of (best_action, value) for this state
    """
    # Update statistics
    stats.nodes_evaluated += 1
    stats.max_depth_reached = max(stats.max_depth_reached, depth)
    
    # Check memoization cache
    cache_key = (n_remaining, current_player)
    if cache_key in _memo_cache:
        return _memo_cache[cache_key]
    
    # Terminal state: n_remaining == 0
    # The player who just moved (previous player) wins
    if n_remaining == 0:
        # Previous player (who made n_remaining = 0) wins
        previous_player = 1 - current_player
        if previous_player == max_player:
            result = (None, 1)  # MAX wins
        else:
            result = (None, -1)  # MAX loses
        _memo_cache[cache_key] = result
        return result
    
    # Generate legal actions
    legal_actions = []
    max_take = min(3, n_remaining)
    for k in range(1, max_take + 1):
        legal_actions.append(k)
    
    if not legal_actions:
        # No moves available (shouldn't happen in Nim except at terminal)
        result = (None, 0)
        _memo_cache[cache_key] = result
        return result
    
    best_action = None
    
    if current_player == max_player:
        # MAX player: maximize value
        best_value = float('-inf')
        for action in legal_actions:
            new_n = n_remaining - action
            next_player = 1 - current_player
            _, value = _minimax_value(new_n, next_player, max_player, depth + 1, stats)
            if value > best_value:
                best_value = value
                best_action = action
    else:
        # MIN player: minimize value
        best_value = float('inf')
        for action in legal_actions:
            new_n = n_remaining - action
            next_player = 1 - current_player
            _, value = _minimax_value(new_n, next_player, max_player, depth + 1, stats)
            if value < best_value:
                best_value = value
                best_action = action
    
    result = (best_action, int(best_value))
    _memo_cache[cache_key] = result
    return result


def minimax_no_cache(game_state, max_player: int = 0) -> Tuple[Optional[int], int, MinimaxStats]:
    """
    Compute minimax without using memoization cache.
    
    Useful for benchmarking and testing.
    
    Args:
        game_state: A NimGame instance
        max_player: The player designated as MAX
        
    Returns:
        Tuple of (best_action, value, stats)
    """
    stats = MinimaxStats()
    start_time = time.perf_counter()
    
    best_action, value = _minimax_value_no_cache(
        n_remaining=game_state.n_remaining,
        current_player=game_state.current_player,
        max_player=max_player,
        depth=0,
        stats=stats
    )
    
    end_time = time.perf_counter()
    stats.elapsed_time_ms = (end_time - start_time) * 1000
    
    return best_action, value, stats


def _minimax_value_no_cache(n_remaining: int, current_player: int, max_player: int,
                             depth: int, stats: MinimaxStats) -> Tuple[Optional[int], int]:
    """
    Recursive minimax without memoization (for benchmarking).
    """
    stats.nodes_evaluated += 1
    stats.max_depth_reached = max(stats.max_depth_reached, depth)
    
    # Terminal state
    if n_remaining == 0:
        previous_player = 1 - current_player
        if previous_player == max_player:
            return (None, 1)
        else:
            return (None, -1)
    
    # Generate legal actions
    legal_actions = list(range(1, min(3, n_remaining) + 1))
    
    if not legal_actions:
        return (None, 0)
    
    best_action = None
    
    if current_player == max_player:
        best_value = float('-inf')
        for action in legal_actions:
            new_n = n_remaining - action
            next_player = 1 - current_player
            _, value = _minimax_value_no_cache(new_n, next_player, max_player, depth + 1, stats)
            if value > best_value:
                best_value = value
                best_action = action
    else:
        best_value = float('inf')
        for action in legal_actions:
            new_n = n_remaining - action
            next_player = 1 - current_player
            _, value = _minimax_value_no_cache(new_n, next_player, max_player, depth + 1, stats)
            if value < best_value:
                best_value = value
                best_action = action
    
    return (best_action, int(best_value))
