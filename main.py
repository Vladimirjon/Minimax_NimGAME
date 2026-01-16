"""
Main Entry Point
Run the Nim game with human and/or AI players.
"""

import nim
import gameAgent
import graphics

def play_game(player0, player1, initial_piles=[1, 3, 5, 7]):
    """
    Play a game of Nim.
    
    Args:
        player0: Agent for player 0
        player1: Agent for player 1
        initial_piles: Starting configuration of piles
    """
    game = nim.Nim(initial_piles)
    players = [player0, player1]
    player_names = [player0.name, player1.name]
    
    graphics.display_welcome()
    
    while not game.is_terminal():
        current_player = players[game.player]
        
        graphics.display_game(game, player_names)
        
        # Get action from current player
        action = current_player.choose_action(game)
        
        # Display the move
        graphics.display_move(current_player.name, action)
        
        # Make the move
        game.move(action)
    
    # Game over - display final state and winner
    graphics.display_game(game, player_names)
    winner = game.winner()
    graphics.display_winner(player_names[winner])

def main():
    """Main function to run the game."""
    print("\nSelect game mode:")
    print("1. Human vs Human")
    print("2. Human vs AI")
    print("3. AI vs Human")
    print("4. AI vs AI")
    
    try:
        choice = input("\nEnter your choice (1-4): ").strip()
    except KeyboardInterrupt:
        print("\nGame cancelled.")
        return
    
    if choice == "1":
        player0 = gameAgent.HumanAgent("Player 1")
        player1 = gameAgent.HumanAgent("Player 2")
    elif choice == "2":
        player0 = gameAgent.HumanAgent("Human")
        player1 = gameAgent.AIAgent("AI")
    elif choice == "3":
        player0 = gameAgent.AIAgent("AI")
        player1 = gameAgent.HumanAgent("Human")
    elif choice == "4":
        player0 = gameAgent.AIAgent("AI 1")
        player1 = gameAgent.AIAgent("AI 2")
    else:
        print("Invalid choice. Defaulting to Human vs AI.")
        player0 = gameAgent.HumanAgent("Human")
        player1 = gameAgent.AIAgent("AI")
    
    # Ask for initial pile configuration (or use default)
    use_default = input("\nUse default pile configuration [1, 3, 5, 7]? (y/n): ").strip().lower()
    
    if use_default == 'y' or use_default == '':
        initial_piles = [1, 3, 5, 7]
    else:
        try:
            piles_input = input("Enter pile sizes separated by spaces (e.g., '3 4 5'): ").strip()
            initial_piles = [int(x) for x in piles_input.split()]
            if not initial_piles or any(p < 0 for p in initial_piles):
                print("Invalid pile configuration. Using default.")
                initial_piles = [1, 3, 5, 7]
        except (ValueError, TypeError):
            print("Invalid input. Using default pile configuration.")
            initial_piles = [1, 3, 5, 7]
    
    play_game(player0, player1, initial_piles)

if __name__ == "__main__":
    main()
