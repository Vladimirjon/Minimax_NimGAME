"""
Paquete del juego de Nim con Minimax AI.

Modulos:
- nim: Logica del juego multi-pila
- minimax: Algoritmo Minimax con Alpha-Beta
- game_agent: Agente inteligente con niveles de dificultad
- graphics: Interfaz grafica PyQt6
- analysis: Herramientas de analisis
"""

from nim import NimGame, Player, GameState
from minimax import MinimaxNim
from game_agent import NimGameAgent, RandomAgent, Difficulty

__all__ = [
    'NimGame',
    'Player',
    'GameState',
    'MinimaxNim',
    'NimGameAgent',
    'RandomAgent',
    'Difficulty'
]
