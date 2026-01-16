# Proyecto 3: Minimax Nim Game (Pyramid UI)

## Overview

This project implements the Minimax decision-making algorithm for the game of Nim. A game agent (`NimGameAgent`) uses Minimax to choose optimal moves. A simple Pygame interface allows a human to play against the agent and visualize the agent’s decisions and performance metrics.

This repository contains:

* `minimax.py` — Minimax implementation (with memoization).
* `gameAgent.py` — Agent wrapper that calls Minimax.
* `nim.py` — Nim environment (rules, moves, victory conditions).
* `graphics.py` — Pygame visualization shows a left-aligned pyramid.
* `main.py` — Entry point and game loop.
* `requirements.txt` — Dependencies.

## Game Rules (Fixed for this project)

We use a  **single-pile take-away Nim** :

1. Initial number of sticks:  **N = 15** .
2. Two players alternate turns.
3. On your turn you must remove **1, 2, or 3** sticks (cannot remove more than the remaining sticks).
4. **Winning condition:** the player who takes the  **last stick wins** .

State definition:

* The game state is represented by one integer: `N_remaining`.

Legal actions:

* `k ∈ {1, 2, 3}` such that `k <= N_remaining`.

Terminal state:

* `N_remaining == 0`.

Winner:

* The player who makes `N_remaining` become `0` is the winner.

## Visual Representation: Left-Aligned Pyramid (3, 5, 7)

Even though the game is  **single-pile** , the UI displays the 15 sticks as a left-aligned pyramid:

* Row 1: 3 sticks
* Row 2: 5 sticks
* Row 3: 7 sticks

Important:

* The pyramid is  **only a visualization** . The real game logic uses `N_remaining`.

Removal visualization policy:

* When a player removes sticks, the UI removes sticks from the  **bottom-most non-empty row** , from  **right to left** , so the pyramid remains visually consistent.

Example:

* Start: (3, 5, 7) = 15
* Take 3: (3, 5, 4) = 12
* Take 2: (3, 5, 2) = 10
* Take 3: (3, 5, 0) = 8

## Optimal Strategy (Mathematical Perspective)

For the move set `{1,2,3}` with “last stick wins” (normal play):

* **Losing positions** are when `N_remaining` is a multiple of 4:
  * `N_remaining ≡ 0 (mod 4)`
* **Winning strategy** is to always leave a multiple of 4 to the opponent.

From any `N` that is not a multiple of 4, the optimal first move is:

* `take = N % 4`

For this project:

* `15 % 4 = 3`
* Optimal first move: **take 3** to leave  **12** .
* After that, respond to the opponent’s move `x` by taking `4 - x` so the total removed in each pair of turns is 4, keeping the opponent on multiples of 4.

Note:

* The agent in this project does not hardcode this rule. It computes optimal play via Minimax. The rule above is included to explain the behavior you will observe.

## Minimax (How it is applied here)

Minimax is used for a two-player, deterministic, perfect-information game:

* MAX player: the agent (by default).
* MIN player: the human (or another agent in autoplay).

Key components:

* **Actions:** remove 1, 2, or 3 sticks.
* **Transition:** `N_remaining -> N_remaining - k`.
* **Terminal:** `N_remaining == 0`.
* **Utility:** from MAX perspective:
  * `+1` if MAX is the player who took the last stick,
  * `-1` if MAX loses.

Performance improvement:

* **Memoization** caches results for `(N_remaining, player_to_move)` to avoid recalculating repeated subtrees.

Collected stats per agent decision:

* `nodes_evaluated`
* `max_depth_reached`
* `elapsed_time_ms`

These are shown in the UI overlay and/or printed in the console.

## Controls (Pygame)

* Key `1`: remove 1 stick
* Key `2`: remove 2 sticks
* Key `3`: remove 3 sticks
* Optional UI buttons may exist (New Game, Auto-Play), depending on implementation.

Invalid moves are rejected (example: trying to remove 3 when only 2 remain).

## How to Run

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Run the game

```bash
python main.py
```

## Optional: Autoplay (Agent vs Agent)

Autoplay mode is used for quick validation and efficiency evaluation. It can:

* run multiple games,
* print average decision time and average nodes evaluated.

If implemented as a CLI flag, example:

```bash
python main.py --autoplay 20
```

## Repository Expectations

* Clear module boundaries:
  * `minimax.py` must not import Pygame.
  * UI code stays in `graphics.py`.
  * Game logic stays in `nim.py`.
* Code should be readable and commented.
* The agent should always play optimally for N=15 under the rules above.

## License / Notes

Academic project. Ensure your submission matches your instructor’s requirements and filenames exactly.
