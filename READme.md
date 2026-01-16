# Minimax Nim Game

A Python implementation of the classic game of Nim with an AI opponent powered by the Minimax algorithm with alpha-beta pruning.

## What is Nim?

Nim is a mathematical strategy game where two players take turns removing objects from distinct piles. On each turn, a player must remove at least one object, and may remove any number of objects from a single pile.

In this implementation, we use the **misère** version of Nim: **the player who takes the last object loses**.

## Features

- 🎮 Multiple game modes:
  - Human vs Human
  - Human vs AI
  - AI vs Human
  - AI vs AI
- 🤖 Optimal AI using Minimax algorithm with alpha-beta pruning
- 🎨 Clean text-based interface
- ⚙️ Configurable pile sizes

## Installation

No external dependencies required! Just Python 3.6+.

```bash
git clone https://github.com/Vladimirjon/Minimax_NimGAME.git
cd Minimax_NimGAME
```

## Usage

Run the game:

```bash
python main.py
```

Follow the on-screen prompts to:
1. Select your game mode (Human vs AI, AI vs AI, etc.)
2. Choose pile configuration (or use default [1, 3, 5, 7])
3. Play the game!

### Playing the Game

When it's your turn:
1. The current game state will be displayed showing all piles
2. Enter the pile number you want to remove from (0-indexed)
3. Enter how many objects to remove from that pile
4. The move will be validated and applied

### Example

```
Choose pile: 2
Choose count: 3
```

This removes 3 objects from pile 2.

## Project Structure

```
.
├── nim.py          # Core game logic and rules
├── minimax.py      # Minimax algorithm with alpha-beta pruning
├── gameAgent.py    # Player agents (Human and AI)
├── graphics.py     # Display and visualization
├── main.py         # Main entry point
└── READme.md       # This file
```

## How the AI Works

The AI uses the **Minimax algorithm** to make optimal moves:

1. **Game Tree**: The algorithm explores all possible future game states
2. **Evaluation**: Each terminal state is evaluated (win = +1, loss = -1)
3. **Minimax**: The AI assumes both players play optimally
4. **Alpha-Beta Pruning**: Eliminates branches that won't affect the final decision, making the algorithm more efficient

The AI will always make the optimal move, making it very challenging to beat!

## Strategy Tips

- In misère Nim, try to leave your opponent in a position where all piles have size 1
- The game has a mathematical solution based on the XOR (nim-sum) of pile sizes
- Against the AI, you'll need perfect play to win (or get lucky with the starting position)

## License

This project is open source and available for educational purposes.

## Author

Vladimirjon
