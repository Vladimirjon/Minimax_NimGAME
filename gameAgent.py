"""
Game Agent
Defines different types of players for the Nim game.
"""

import minimax

class Agent:
    """Base class for game agents."""
    
    def __init__(self, name):
        self.name = name
    
    def choose_action(self, game):
        """
        Choose an action given the current game state.
        
        Args:
            game: Current game state (Nim object)
            
        Returns:
            Action (pile, count) tuple
        """
        raise NotImplementedError

class HumanAgent(Agent):
    """Agent that asks for human input."""
    
    def __init__(self, name="Human"):
        super().__init__(name)
    
    def choose_action(self, game):
        """
        Get action from human player via console input.
        
        Args:
            game: Current game state (Nim object)
            
        Returns:
            Action (pile, count) tuple
        """
        available = game.available_actions()
        
        while True:
            try:
                pile = int(input("Choose pile: "))
                count = int(input("Choose count: "))
                action = (pile, count)
                
                if action in available:
                    return action
                else:
                    print("Invalid move. Try again.")
            except (ValueError, KeyboardInterrupt):
                print("Invalid input. Try again.")

class AIAgent(Agent):
    """Agent that uses minimax algorithm."""
    
    def __init__(self, name="AI"):
        super().__init__(name)
    
    def choose_action(self, game):
        """
        Choose the optimal action using minimax algorithm.
        
        Args:
            game: Current game state (Nim object)
            
        Returns:
            Action (pile, count) tuple
        """
        action = minimax.get_best_move(game)
        return action
