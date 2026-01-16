"""
nim.py - Nim Game Environment

This module implements the single-pile Nim game with the following rules:
- Initial sticks: N = 15
- Legal moves: remove 1, 2, or 3 sticks (if available)
- Winning condition: player who takes the last stick wins (normal play)
"""


class NimGame:
    """
    Represents the state of a single-pile Nim game.
    
    Attributes:
        n_remaining: Number of sticks remaining in the pile
        current_player: 0 (MAX/Agent) or 1 (MIN/Human)
        last_player: The player who made the last move (used to determine winner)
    """
    
    INITIAL_STICKS = 15
    MAX_TAKE = 3
    MIN_TAKE = 1
    
    # Player constants
    PLAYER_MAX = 0  # Agent (MAX player in minimax)
    PLAYER_MIN = 1  # Human (MIN player in minimax)
    
    def __init__(self, n_remaining: int = None, current_player: int = None):
        """
        Initialize a new Nim game state.
        
        Args:
            n_remaining: Number of sticks (defaults to INITIAL_STICKS)
            current_player: Starting player (defaults to PLAYER_MAX)
        """
        self.n_remaining = n_remaining if n_remaining is not None else self.INITIAL_STICKS
        self.current_player = current_player if current_player is not None else self.PLAYER_MAX
        self.last_player = None  # Track who made the last move
    
    def get_legal_actions(self) -> list:
        """
        Returns list of legal actions from current state.
        
        An action k is legal if 1 <= k <= min(3, n_remaining).
        
        Returns:
            List of integers representing legal moves [1], [1,2], or [1,2,3]
        """
        if self.n_remaining <= 0:
            return []
        
        max_take = min(self.MAX_TAKE, self.n_remaining)
        return list(range(self.MIN_TAKE, max_take + 1))
    
    def apply_action(self, k: int) -> 'NimGame':
        """
        Apply action k to create a new game state.
        
        Args:
            k: Number of sticks to remove (1, 2, or 3)
            
        Returns:
            New NimGame instance with updated state
            
        Raises:
            ValueError: If action is not legal
        """
        if k not in self.get_legal_actions():
            raise ValueError(f"Illegal action: {k}. Legal actions: {self.get_legal_actions()}")
        
        new_game = NimGame(
            n_remaining=self.n_remaining - k,
            current_player=1 - self.current_player  # Switch player
        )
        new_game.last_player = self.current_player  # The current player made this move
        return new_game
    
    def apply_action_inplace(self, k: int) -> None:
        """
        Apply action k to the current game state (in-place modification).
        
        Args:
            k: Number of sticks to remove (1, 2, or 3)
            
        Raises:
            ValueError: If action is not legal
        """
        if k not in self.get_legal_actions():
            raise ValueError(f"Illegal action: {k}. Legal actions: {self.get_legal_actions()}")
        
        self.n_remaining -= k
        self.last_player = self.current_player
        self.current_player = 1 - self.current_player  # Switch player
    
    def is_terminal(self) -> bool:
        """
        Check if the game has ended.
        
        Returns:
            True if n_remaining == 0, False otherwise
        """
        return self.n_remaining == 0
    
    def winner(self) -> int:
        """
        Determine the winner of the game.
        
        Returns:
            The player who took the last stick (if terminal), or None if game not over
        """
        if not self.is_terminal():
            return None
        return self.last_player  # The player who made n_remaining = 0 wins
    
    def clone(self) -> 'NimGame':
        """
        Create a deep copy of the current game state.
        
        Returns:
            New NimGame instance with same state
        """
        new_game = NimGame(
            n_remaining=self.n_remaining,
            current_player=self.current_player
        )
        new_game.last_player = self.last_player
        return new_game
    
    def utility(self, max_player: int = PLAYER_MAX) -> int:
        """
        Compute utility value from MAX player's perspective.
        
        Args:
            max_player: The player designated as MAX (default: PLAYER_MAX)
            
        Returns:
            +1 if MAX player won, -1 if MAX player lost, 0 if game not over
        """
        if not self.is_terminal():
            return 0
        
        winner = self.winner()
        if winner == max_player:
            return 1
        else:
            return -1
    
    def __repr__(self) -> str:
        player_name = "MAX" if self.current_player == self.PLAYER_MAX else "MIN"
        return f"NimGame(sticks={self.n_remaining}, player={player_name})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, NimGame):
            return False
        return (self.n_remaining == other.n_remaining and 
                self.current_player == other.current_player)
    
    def __hash__(self) -> int:
        return hash((self.n_remaining, self.current_player))


def get_pyramid_representation(n_remaining: int) -> tuple:
    """
    Convert n_remaining to pyramid row counts for visualization.
    
    The pyramid has rows of 3, 5, 7 sticks (bottom-up removal from right to left).
    
    Args:
        n_remaining: Number of sticks remaining
        
    Returns:
        Tuple of (row1_count, row2_count, row3_count) where row3 is bottom
    """
    if n_remaining <= 0:
        return (0, 0, 0)
    
    # Full pyramid: row1=3, row2=5, row3=7, total=15
    # Remove from bottom (row3) first, then row2, then row1
    
    removed = 15 - n_remaining
    
    row3 = 7
    row2 = 5
    row1 = 3
    
    # Remove from row3 first (bottom)
    if removed <= 7:
        row3 = 7 - removed
    else:
        row3 = 0
        removed -= 7
        # Remove from row2
        if removed <= 5:
            row2 = 5 - removed
        else:
            row2 = 0
            removed -= 5
            # Remove from row1
            row1 = max(0, 3 - removed)
    
    return (row1, row2, row3)
