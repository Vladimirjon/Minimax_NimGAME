"""
main.py - Nim Game Entry Point

This is the main entry point for the Nim game. It provides:
- Human vs Agent mode (default)
- Agent vs Agent autoplay mode for testing
- Performance experiments
"""

import argparse
import time
import sys
from typing import List, Tuple

from nim import NimGame
from gameAgent import NimGameAgent
from minimax import clear_memo_cache


def run_game_human_vs_agent():
    """
    Run the interactive Human vs Agent game with Pygame UI.
    
    The agent plays as MAX (player 0) and goes first.
    The human plays as MIN (player 1) and responds.
    """
    # Import graphics here to avoid loading Pygame for autoplay mode
    from graphics import NimGraphics
    
    graphics = NimGraphics()
    game = NimGame()
    agent = NimGameAgent(player_id=NimGame.PLAYER_MAX)
    
    running = True
    agent_thinking = False
    think_delay = 0
    
    while running:
        # Handle events
        action = graphics.get_human_action()
        
        if action == 'quit':
            running = False
            continue
        elif action == 'reset':
            game = NimGame()
            agent.reset()
            clear_memo_cache()
            graphics.clear_message()
            graphics.last_agent_stats = None
            graphics.last_agent_action = None
            continue
        
        # Game over check
        if game.is_terminal():
            graphics.draw(game)
            graphics.tick()
            continue
        
        # Agent's turn (MAX player)
        if game.current_player == NimGame.PLAYER_MAX:
            if not agent_thinking:
                agent_thinking = True
                think_delay = 30  # Short delay before agent moves (about 0.5 second)
            
            if think_delay > 0:
                think_delay -= 1
            else:
                # Agent makes a move
                agent_action, stats = agent.choose_action(game)
                game.apply_action_inplace(agent_action)
                graphics.update_agent_stats(agent_action, stats)
                graphics.set_message(f"Agent takes {agent_action} stick(s)")
                agent_thinking = False
        
        # Human's turn (MIN player)
        elif game.current_player == NimGame.PLAYER_MIN:
            if action in [1, 2, 3]:
                legal = game.get_legal_actions()
                if action in legal:
                    game.apply_action_inplace(action)
                    graphics.clear_message()
                else:
                    graphics.show_invalid_move_feedback()
        
        graphics.draw(game)
        graphics.tick()
    
    graphics.quit()


def run_autoplay(num_games: int = 20, verbose: bool = True) -> List[dict]:
    """
    Run Agent vs Agent autoplay games for testing and statistics.
    
    Args:
        num_games: Number of games to play
        verbose: Whether to print game details
        
    Returns:
        List of game statistics dictionaries
    """
    results = []
    
    for game_num in range(num_games):
        # Create fresh game and agents
        game = NimGame()
        agent_max = NimGameAgent(player_id=NimGame.PLAYER_MAX)
        agent_min = NimGameAgent(player_id=NimGame.PLAYER_MIN)
        
        clear_memo_cache()
        
        game_stats = {
            'game_num': game_num + 1,
            'moves': [],
            'total_nodes': 0,
            'total_time_ms': 0.0,
            'winner': None
        }
        
        if verbose:
            print(f"\n=== Game {game_num + 1} ===")
            print(f"Starting sticks: {game.n_remaining}")
        
        move_count = 0
        while not game.is_terminal():
            current_agent = agent_max if game.current_player == NimGame.PLAYER_MAX else agent_min
            player_name = "MAX" if game.current_player == NimGame.PLAYER_MAX else "MIN"
            
            action, stats = current_agent.choose_action(game)
            
            move_stats = {
                'player': player_name,
                'sticks_before': game.n_remaining,
                'action': action,
                'nodes': stats.nodes_evaluated,
                'time_ms': stats.elapsed_time_ms
            }
            game_stats['moves'].append(move_stats)
            game_stats['total_nodes'] += stats.nodes_evaluated
            game_stats['total_time_ms'] += stats.elapsed_time_ms
            
            if verbose:
                print(f"  {player_name}: Take {action} (from {game.n_remaining}) -> "
                      f"{game.n_remaining - action} | nodes={stats.nodes_evaluated}, "
                      f"time={stats.elapsed_time_ms:.3f}ms")
            
            game.apply_action_inplace(action)
            move_count += 1
        
        winner = "MAX" if game.winner() == NimGame.PLAYER_MAX else "MIN"
        game_stats['winner'] = winner
        
        if verbose:
            print(f"  Winner: {winner}")
        
        results.append(game_stats)
    
    return results


def run_experiments():
    """
    Run efficiency evaluation experiments.
    
    Plays 20 autoplay games and prints average statistics.
    """
    print("=" * 60)
    print("MINIMAX NIM GAME - EFFICIENCY EXPERIMENTS")
    print("=" * 60)
    print("\nRunning 20 autoplay games...")
    print("(Agent vs Agent, both using Minimax)")
    
    results = run_autoplay(num_games=20, verbose=False)
    
    # Calculate averages
    total_nodes = sum(r['total_nodes'] for r in results)
    total_time = sum(r['total_time_ms'] for r in results)
    total_moves = sum(len(r['moves']) for r in results)
    max_wins = sum(1 for r in results if r['winner'] == 'MAX')
    
    avg_nodes_per_game = total_nodes / len(results)
    avg_time_per_game = total_time / len(results)
    avg_nodes_per_move = total_nodes / total_moves if total_moves > 0 else 0
    avg_time_per_move = total_time / total_moves if total_moves > 0 else 0
    
    print("\n" + "=" * 60)
    print("EXPERIMENT RESULTS (20 Games)")
    print("=" * 60)
    print(f"\nGame Statistics:")
    print(f"  - Games played: {len(results)}")
    print(f"  - MAX wins: {max_wins} ({max_wins / len(results) * 100:.1f}%)")
    print(f"  - MIN wins: {len(results) - max_wins} ({(len(results) - max_wins) / len(results) * 100:.1f}%)")
    print(f"  - Total moves: {total_moves}")
    print(f"  - Average moves per game: {total_moves / len(results):.1f}")
    
    print(f"\nPerformance Metrics:")
    print(f"  - Average nodes evaluated per game: {avg_nodes_per_game:.1f}")
    print(f"  - Average nodes evaluated per move: {avg_nodes_per_move:.1f}")
    print(f"  - Average decision time per game: {avg_time_per_game:.3f} ms")
    print(f"  - Average decision time per move: {avg_time_per_move:.3f} ms")
    print(f"  - Total computation time: {total_time:.3f} ms")
    
    print("\nNote: With memoization enabled, subsequent games benefit from cached results.")
    print("      The first game populates the cache, making later decisions faster.")
    
    # Run without cache to show difference
    print("\n" + "-" * 60)
    print("Running 3 games WITHOUT memoization cache for comparison...")
    
    from minimax import minimax_no_cache
    clear_memo_cache()
    
    no_cache_results = []
    for i in range(3):
        game = NimGame()
        total_nodes = 0
        total_time = 0
        
        while not game.is_terminal():
            best_action, value, stats = minimax_no_cache(game, max_player=game.current_player)
            total_nodes += stats.nodes_evaluated
            total_time += stats.elapsed_time_ms
            game.apply_action_inplace(best_action)
        
        no_cache_results.append({'nodes': total_nodes, 'time': total_time})
    
    avg_nodes_no_cache = sum(r['nodes'] for r in no_cache_results) / len(no_cache_results)
    avg_time_no_cache = sum(r['time'] for r in no_cache_results) / len(no_cache_results)
    
    print(f"\nWithout Memoization (average of 3 games):")
    print(f"  - Average nodes evaluated per game: {avg_nodes_no_cache:.1f}")
    print(f"  - Average decision time per game: {avg_time_no_cache:.3f} ms")
    print(f"\nMemoization speedup: {avg_nodes_no_cache / avg_nodes_per_game:.1f}x fewer nodes")
    
    print("\n" + "=" * 60)
    print("STRATEGY VERIFICATION")
    print("=" * 60)
    print("\nOptimal strategy for N=15 with moves {1,2,3} (last-takes-wins):")
    print("  - Leave opponent on multiples of 4")
    print("  - First player (MAX) should take 3 to leave 12")
    print("  - Then always take (4 - opponent's move)")
    print("\nVerifying agent's first move...")
    
    clear_memo_cache()
    game = NimGame()
    agent = NimGameAgent(player_id=NimGame.PLAYER_MAX)
    first_action, stats = agent.choose_action(game)
    
    print(f"  Agent's first move: Take {first_action}")
    print(f"  Expected: Take 3 (to leave 12)")
    print(f"  Result: {'CORRECT!' if first_action == 3 else 'INCORRECT'}")
    
    print("\n" + "=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Nim Game with Minimax AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                # Interactive Human vs Agent game
  python main.py --autoplay 10  # Run 10 Agent vs Agent games
  python main.py --experiments  # Run efficiency experiments
        """
    )
    
    parser.add_argument(
        '--autoplay',
        type=int,
        metavar='N',
        help='Run N autoplay games (Agent vs Agent)'
    )
    
    parser.add_argument(
        '--experiments',
        action='store_true',
        help='Run efficiency evaluation experiments'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Reduce output verbosity for autoplay'
    )
    
    args = parser.parse_args()
    
    if args.experiments:
        run_experiments()
    elif args.autoplay:
        print(f"Running {args.autoplay} autoplay games...")
        results = run_autoplay(num_games=args.autoplay, verbose=not args.quiet)
        
        if args.quiet:
            max_wins = sum(1 for r in results if r['winner'] == 'MAX')
            avg_time = sum(r['total_time_ms'] for r in results) / len(results)
            print(f"\nSummary: MAX won {max_wins}/{len(results)}, avg time: {avg_time:.3f}ms/game")
    else:
        run_game_human_vs_agent()


if __name__ == "__main__":
    main()
