"""
Agente de juego que utiliza el algoritmo Minimax para jugar Nim multi-pila.

El agente tiene diferentes niveles de dificultad con comportamiento consistente.
"""

from typing import Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import random

from nim import NimGame, Player
from minimax import MinimaxNim


class Difficulty(Enum):
    """Niveles de dificultad del agente."""
    EASY = "Facil"
    MEDIUM = "Medio"
    HARD = "Dificil"
    OPTIMAL = "Optimo"


@dataclass
class AgentStatistics:
    """Estadisticas del agente durante una sesion."""
    games_played: int = 0
    games_won: int = 0
    
    def reset(self) -> None:
        """Reinicia las estadisticas."""
        self.games_played = 0
        self.games_won = 0
    
    def record_game_result(self, won: bool) -> None:
        """Registra el resultado de una partida."""
        self.games_played += 1
        if won:
            self.games_won += 1
    
    def get_win_rate(self) -> float:
        """Calcula la tasa de victorias en porcentaje."""
        if self.games_played == 0:
            return 0.0
        return (self.games_won / self.games_played) * 100


class NimGameAgent:
    """
    Agente inteligente que juega Nim usando el algoritmo Minimax.
    
    Niveles de dificultad:
    - EASY: 20% movimientos optimos, 80% aleatorios
    - MEDIUM: 50% movimientos optimos, 50% aleatorios
    - HARD: 80% movimientos optimos, 20% aleatorios
    - OPTIMAL: 100% movimientos optimos (usa Nim-sum directamente)
    
    La diferencia con la version anterior es que el agente OPTIMAL
    siempre usa la estrategia matematica de Nim-sum, garantizando
    consistencia total en su comportamiento.
    """
    
    DIFFICULTY_PROBABILITIES = {
        Difficulty.EASY: 0.20,
        Difficulty.MEDIUM: 0.50,
        Difficulty.HARD: 0.80,
        Difficulty.OPTIMAL: 1.00
    }
    
    def __init__(self, game: NimGame, difficulty: str = 'optimal'):
        """
        Inicializa el agente de juego.
        
        Args:
            game: Instancia del juego de Nim.
            difficulty: Nivel de dificultad.
        """
        self.game = game
        self.set_difficulty(difficulty)
        self.minimax = MinimaxNim(game)
        self.stats = AgentStatistics()
    
    def set_difficulty(self, difficulty: str) -> None:
        """
        Establece el nivel de dificultad del agente.
        
        Args:
            difficulty: Nombre del nivel de dificultad.
        """
        difficulty_map = {
            'facil': Difficulty.EASY,
            'easy': Difficulty.EASY,
            'medio': Difficulty.MEDIUM,
            'medium': Difficulty.MEDIUM,
            'dificil': Difficulty.HARD,
            'hard': Difficulty.HARD,
            'optimo': Difficulty.OPTIMAL,
            'optimal': Difficulty.OPTIMAL
        }
        self.difficulty = difficulty_map.get(difficulty.lower(), Difficulty.OPTIMAL)
    
    def get_difficulty_name(self) -> str:
        """Retorna el nombre de la dificultad actual."""
        return self.difficulty.value
    
    def get_move(self) -> Optional[Tuple[int, int]]:
        """
        Obtiene el movimiento del agente para el estado actual.
        
        Returns:
            Tupla (pile_index, sticks) o None si no hay movimientos.
        """
        piles = self.game.get_piles()
        
        if self.game.is_terminal(piles):
            return None
        
        # Para dificultad OPTIMAL, siempre usar estrategia matematica
        if self.difficulty == Difficulty.OPTIMAL:
            return self._get_optimal_move(piles)
        
        # Para otras dificultades, decidir probabilisticamente
        use_optimal = random.random() < self.DIFFICULTY_PROBABILITIES[self.difficulty]
        
        if use_optimal:
            return self._get_optimal_move(piles)
        else:
            return self._get_random_move(piles)
    
    def _get_optimal_move(self, piles: List[int]) -> Tuple[int, int]:
        """
        Obtiene el movimiento optimo.
        
        Primero intenta usar la estrategia matematica de Nim-sum.
        Si no hay movimiento optimo (posicion perdedora), usa Minimax
        para minimizar el dano.
        
        Args:
            piles: Estado actual de las pilas.
        
        Returns:
            Tupla (pile_index, sticks).
        """
        # Intentar estrategia matematica primero (mas eficiente)
        optimal = self.game.get_optimal_move(piles)
        
        if optimal is not None:
            return optimal
        
        # Si estamos en posicion perdedora, usar Minimax para mejor respuesta
        minimax_move = self.minimax.get_best_move(piles, is_maximizing=True)
        
        if minimax_move is not None:
            return minimax_move
        
        # Fallback: movimiento aleatorio
        return self._get_random_move(piles)
    
    def _get_random_move(self, piles: List[int]) -> Tuple[int, int]:
        """
        Obtiene un movimiento aleatorio valido.
        
        Args:
            piles: Estado actual de las pilas.
        
        Returns:
            Tupla (pile_index, sticks).
        """
        valid_moves = self.game.get_valid_moves(piles)
        
        if not valid_moves:
            # No deberia ocurrir, pero por seguridad
            for i, p in enumerate(piles):
                if p > 0:
                    return (i, 1)
            return (0, 1)
        
        return random.choice(valid_moves)
    
    def get_statistics(self) -> dict:
        """
        Obtiene las estadisticas del agente.
        
        Returns:
            Diccionario con estadisticas.
        """
        return {
            'difficulty': self.difficulty.value,
            'games_played': self.stats.games_played,
            'games_won': self.stats.games_won,
            'win_rate': round(self.stats.get_win_rate(), 1)
        }
    
    def reset_statistics(self) -> None:
        """Reinicia las estadisticas del agente."""
        self.stats.reset()
        self.minimax.clear_cache()
    
    def notify_game_end(self, won: bool) -> None:
        """
        Notifica al agente que la partida termino.
        
        Args:
            won: True si el agente gano la partida.
        """
        self.stats.record_game_result(won)


class RandomAgent:
    """Agente que juega de forma completamente aleatoria."""
    
    def __init__(self, game: NimGame):
        """Inicializa el agente aleatorio."""
        self.game = game
        self.stats = AgentStatistics()
    
    def get_move(self) -> Optional[Tuple[int, int]]:
        """Obtiene un movimiento aleatorio valido."""
        piles = self.game.get_piles()
        valid_moves = self.game.get_valid_moves(piles)
        
        if not valid_moves:
            return None
        
        return random.choice(valid_moves)
    
    def get_statistics(self) -> dict:
        """Retorna estadisticas basicas."""
        return {
            'difficulty': 'Aleatorio',
            'games_played': self.stats.games_played,
            'games_won': self.stats.games_won,
            'win_rate': round(self.stats.get_win_rate(), 1)
        }
    
    def notify_game_end(self, won: bool) -> None:
        """Notifica el resultado de la partida."""
        self.stats.record_game_result(won)
