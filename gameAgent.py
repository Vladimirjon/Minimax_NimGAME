"""
gameAgent.py - Nim Game Agent

This module implements the NimGameAgent class that uses the Minimax algorithm
to make optimal decisions in the Nim game.
"""

from typing import Tuple, Optional
from nim import NimGame
from minimax import minimax, MinimaxStats, clear_memo_cache


class NimGameAgent:
    """
    An AI agent that plays the Nim game using the Minimax algorithm.
    
    The agent computes the optimal action for any game state by evaluating
    all possible game outcomes using minimax with memoization.
    
    Attributes:
        player_id: The player ID this agent plays as (0 = MAX, 1 = MIN)
        last_stats: Statistics from the most recent decision
    """
    
    def __init__(self, player_id: int = 0):
        """
        Initialize the game agent.
        
        Args:
            player_id: The player ID this agent represents (default: 0 = MAX)
        """
        self.player_id = player_id
        self.last_stats: Optional[MinimaxStats] = None
    
    def choose_action(self, game_state: NimGame) -> Tuple[int, MinimaxStats]:
        """
        Choose the optimal action for the given game state.
        
        Uses the Minimax algorithm to evaluate all possible moves and
        selects the one with the best expected outcome.
        
        Args:
            game_state: The current NimGame state
            
        Returns:
            Tuple of (action, stats) where:
            - action: The optimal number of sticks to remove (1, 2, or 3)
            - stats: MinimaxStats with performance metrics
            
        Raises:
            ValueError: If the game is already in a terminal state
        """
        if game_state.is_terminal():
            raise ValueError("Cannot choose action: game is already over")
        
        if game_state.current_player != self.player_id:
            raise ValueError(f"Not agent's turn. Current player: {game_state.current_player}, "
                           f"Agent player: {self.player_id}")
        
        # Compute optimal action using minimax
        best_action, value, stats = minimax(game_state, max_player=self.player_id)
        
        self.last_stats = stats
        
        return best_action, stats
    
    def get_last_stats(self) -> Optional[MinimaxStats]:
        """
        Get the statistics from the most recent decision.
        
        Returns:
            MinimaxStats instance or None if no decision has been made
        """
        return self.last_stats
    
    def reset(self):
        """Reset the agent state (clears last stats)."""
        self.last_stats = None
    
    @staticmethod
    def clear_cache():
        """Clear the minimax memoization cache."""
        clear_memo_cache()
    
    def __repr__(self) -> str:
        return f"NimGameAgent(player_id={self.player_id})"


class RandomAgent:
    """
    A simple agent that makes random legal moves.
    Useful for testing and demonstration.
    """
    
    def __init__(self, player_id: int = 0):
        """
        Initialize the random agent.
        
        Args:
            player_id: The player ID this agent represents
        """
        self.player_id = player_id
        self.last_stats = None
    
    def choose_action(self, game_state: NimGame) -> Tuple[int, None]:
        """
        Choose a random legal action.
        
        Args:
            game_state: The current NimGame state
            
        Returns:
            Tuple of (action, None) - no stats for random agent
        """
        import random
        
        if game_state.is_terminal():
            raise ValueError("Cannot choose action: game is already over")
        
        legal_actions = game_state.get_legal_actions()
        action = random.choice(legal_actions)
        
        return action, None
    
    def __repr__(self) -> str:
        return f"RandomAgent(player_id={self.player_id})"
