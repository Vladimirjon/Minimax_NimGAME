"""
Graphics and Display
Simple text-based visualization for the Nim game.
"""

def display_game(game, player_names=None):
    """
    Display the current game state in a nice format.
    
    Args:
        game: Current game state (Nim object)
        player_names: Optional list of player names [player0, player1]
    """
    print("\n" + "=" * 40)
    print("GAME STATE")
    print("=" * 40)
    print(str(game))
    print("=" * 40)
    
    if player_names:
        print(f"Current player: {player_names[game.player]}")
    else:
        print(f"Current player: Player {game.player}")
    print()

def display_move(player_name, action):
    """
    Display a move that was made.
    
    Args:
        player_name: Name of the player who made the move
        action: Action (pile, count) tuple
    """
    pile, count = action
    print(f"\n{player_name} removes {count} object(s) from pile {pile}")

def display_winner(winner_name):
    """
    Display the winner of the game.
    
    Args:
        winner_name: Name of the winning player
    """
    print("\n" + "=" * 40)
    print(f"🎉 {winner_name} WINS! 🎉")
    print("=" * 40)

def display_welcome():
    """Display welcome message."""
    print("\n" + "=" * 40)
    print("WELCOME TO NIM!")
    print("=" * 40)
    print("Rules:")
    print("- Players take turns removing objects from piles")
    print("- On your turn, remove any number of objects from a single pile")
    print("- The player who takes the LAST object LOSES")
    print("=" * 40)
