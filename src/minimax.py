"""
Implementacion del algoritmo Minimax con poda Alpha-Beta para Nim multi-pila.

Este modulo proporciona una implementacion optimizada del algoritmo Minimax
con memoizacion para el juego de Nim con multiples pilas.
"""

from typing import Tuple, Optional, Dict, List
from dataclasses import dataclass
import time


@dataclass
class MinimaxStatistics:
    """Estadisticas de ejecucion del algoritmo Minimax."""
    nodes_evaluated: int = 0
    max_depth_reached: int = 0
    cache_hits: int = 0
    elapsed_time_ms: float = 0.0
    
    def reset(self) -> None:
        """Reinicia todas las estadisticas."""
        self.nodes_evaluated = 0
        self.max_depth_reached = 0
        self.cache_hits = 0
        self.elapsed_time_ms = 0.0
    
    def to_dict(self) -> dict:
        """Convierte las estadisticas a diccionario."""
        return {
            'nodes_evaluated': self.nodes_evaluated,
            'max_depth_reached': self.max_depth_reached,
            'cache_hits': self.cache_hits,
            'elapsed_time_ms': round(self.elapsed_time_ms, 4)
        }


class MinimaxNim:
    """
    Implementacion de Minimax con Alpha-Beta y memoizacion para Nim multi-pila.
    
    Attributes:
        game: Referencia al juego de Nim.
        stats: Estadisticas de ejecucion.
        cache: Diccionario para memoizacion.
    """
    
    def __init__(self, game):
        """
        Inicializa el algoritmo Minimax.
        
        Args:
            game: Instancia del juego de Nim.
        """
        self.game = game
        self.stats = MinimaxStatistics()
        self.cache: Dict[Tuple, int] = {}
    
    def clear_cache(self) -> None:
        """Limpia el cache de memoizacion."""
        self.cache.clear()
    
    def get_best_move(self, piles: List[int], is_maximizing: bool) -> Optional[Tuple[int, int]]:
        """
        Encuentra el mejor movimiento para el estado actual.
        
        Args:
            piles: Estado actual de las pilas.
            is_maximizing: True si es el turno del jugador maximizador.
        
        Returns:
            Tupla (pile_index, sticks) o None si no hay movimientos.
        """
        self.stats.reset()
        start_time = time.perf_counter()
        
        best_move = None
        best_value = float('-inf') if is_maximizing else float('inf')
        alpha = float('-inf')
        beta = float('inf')
        
        valid_moves = self.game.get_valid_moves(piles)
        
        if not valid_moves:
            return None
        
        for move in valid_moves:
            pile_idx, sticks = move
            new_piles = self.game.apply_move(piles, pile_idx, sticks)
            value = self._minimax(new_piles, 0, alpha, beta, not is_maximizing)
            
            if is_maximizing:
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, value)
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, value)
        
        self.stats.elapsed_time_ms = (time.perf_counter() - start_time) * 1000
        return best_move
    
    def _minimax(self, piles: List[int], depth: int,
                 alpha: float, beta: float, is_maximizing: bool) -> int:
        """
        Funcion recursiva de Minimax con Alpha-Beta y memoizacion.
        
        Args:
            piles: Estado actual de las pilas.
            depth: Profundidad actual en el arbol.
            alpha: Mejor valor para el maximizador.
            beta: Mejor valor para el minimizador.
            is_maximizing: True si es turno del maximizador.
        
        Returns:
            Valor de evaluacion del estado (-1 o 1).
        """
        # Verificar cache
        cache_key = (tuple(piles), is_maximizing)
        if cache_key in self.cache:
            self.stats.cache_hits += 1
            return self.cache[cache_key]
        
        self.stats.nodes_evaluated += 1
        self.stats.max_depth_reached = max(self.stats.max_depth_reached, depth)
        
        # Estado terminal
        if self.game.is_terminal(piles):
            # El jugador anterior gano (tomo el ultimo palito)
            result = -1 if is_maximizing else 1
            self.cache[cache_key] = result
            return result
        
        valid_moves = self.game.get_valid_moves(piles)
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                pile_idx, sticks = move
                new_piles = self.game.apply_move(piles, pile_idx, sticks)
                eval_value = self._minimax(new_piles, depth + 1, alpha, beta, False)
                max_eval = max(max_eval, eval_value)
                alpha = max(alpha, eval_value)
                if beta <= alpha:
                    break
            self.cache[cache_key] = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                pile_idx, sticks = move
                new_piles = self.game.apply_move(piles, pile_idx, sticks)
                eval_value = self._minimax(new_piles, depth + 1, alpha, beta, True)
                min_eval = min(min_eval, eval_value)
                beta = min(beta, eval_value)
                if beta <= alpha:
                    break
            self.cache[cache_key] = min_eval
            return min_eval
    
    def get_statistics(self) -> MinimaxStatistics:
        """Retorna las estadisticas de la ultima ejecucion."""
        return self.stats
