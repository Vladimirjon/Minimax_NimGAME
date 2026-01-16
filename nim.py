"""
Nim Game Logic
A simple implementation of the game of Nim.
"""

class Nim:
    """
    Represents the Nim game state.
    In Nim, players take turns removing objects from distinct piles.
    On each turn, a player must remove at least one object, and may remove any number of objects
    from a single pile. The player who takes the last object loses (misère version).
    """
    
    def __init__(self, piles=[1, 3, 5, 7]):
        """
        Initialize a Nim game with the given piles.
        
        Args:
            piles: List of integers representing the number of objects in each pile
        """
        self.piles = piles.copy()
        self.player = 0  # 0 or 1
        
    def available_actions(self):
        """
        Returns a set of all available actions (pile, count) tuples.
        An action is removing 'count' objects from 'pile'.
        """
        actions = set()
        for i, pile in enumerate(self.piles):
            for count in range(1, pile + 1):
                actions.add((i, count))
        return actions
    
    def other_player(self, player):
        """
        Returns the opponent of the given player.
        """
        return 0 if player == 1 else 1
    
    def switch_player(self):
        """
        Switch to the other player.
        """
        self.player = self.other_player(self.player)
    
    def move(self, action):
        """
        Make a move by removing objects from a pile.
        
        Args:
            action: Tuple (pile, count) representing the move
        """
        pile, count = action
        
        # Validate the move
        if pile < 0 or pile >= len(self.piles):
            raise ValueError("Invalid pile")
        if count < 1 or count > self.piles[pile]:
            raise ValueError("Invalid number of objects")
        
        # Make the move
        self.piles[pile] -= count
        self.switch_player()
    
    def is_terminal(self):
        """
        Returns True if the game is over (all piles are empty).
        """
        return all(pile == 0 for pile in self.piles)
    
    def winner(self):
        """
        Returns the winner of the game.
        In misère Nim, the player who takes the last object loses.
        Returns None if the game is not over.
        """
        if not self.is_terminal():
            return None
        # The current player took the last object and loses
        return self.other_player(self.player)
    
    def __str__(self):
        """
        String representation of the game state.
        """
        result = []
        for i, pile in enumerate(self.piles):
            result.append(f"Pile {i}: {'|' * pile} ({pile})")
        return "\n".join(result)
