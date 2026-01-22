"""
Implementacion del juego de Nim con multiples pilas.

Reglas:
- Estado inicial: 3 filas con 3, 5 y 7 palitos respectivamente
- Movimientos validos: elegir una fila y remover de 1 a 3 palitos
- Condicion de victoria: el jugador que toma el ultimo palito gana
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class Player(Enum):
    """Enumeracion que representa los jugadores del juego."""
    HUMAN = 1
    AGENT = 2


@dataclass
class GameState:
    """
    Clase que encapsula el estado del juego.
    
    Attributes:
        piles: Lista con el numero de palitos en cada fila.
        current_player: Jugador que tiene el turno actual.
        move_history: Lista de movimientos realizados.
    """
    piles: List[int]
    current_player: Player
    move_history: List[Tuple[Player, int, int]]
    
    def copy(self) -> 'GameState':
        """Crea una copia profunda del estado actual."""
        return GameState(
            piles=self.piles.copy(),
            current_player=self.current_player,
            move_history=self.move_history.copy()
        )
    
    def to_tuple(self) -> Tuple[int, ...]:
        """Convierte el estado a tupla para uso como clave de cache."""
        return tuple(self.piles)


class NimGame:
    """
    Clase principal que implementa la logica del juego de Nim multi-pila.
    
    El juego sigue las reglas clasicas de Nim donde:
    - Se inicia con 3 filas de 3, 5 y 7 palitos
    - Cada jugador puede remover de 1 a 3 palitos de una fila elegida
    - El jugador que toma el ultimo palito gana
    """
    
    INITIAL_PILES = [3, 5, 7]
    MAX_TAKE = 3
    MIN_TAKE = 1
    
    def __init__(self, initial_piles: List[int] = None):
        """
        Inicializa una nueva instancia del juego de Nim.
        
        Args:
            initial_piles: Configuracion inicial de pilas. Por defecto [3, 5, 7].
        """
        self.initial_piles = initial_piles if initial_piles else self.INITIAL_PILES.copy()
        self.state = self._create_initial_state()
    
    def _create_initial_state(self) -> GameState:
        """Crea el estado inicial del juego."""
        return GameState(
            piles=self.initial_piles.copy(),
            current_player=Player.HUMAN,
            move_history=[]
        )
    
    def reset(self) -> None:
        """Reinicia el juego a su estado inicial."""
        self.state = self._create_initial_state()
    
    def get_piles(self) -> List[int]:
        """Retorna el estado actual de las pilas."""
        return self.state.piles.copy()
    
    def get_pile(self, index: int) -> int:
        """Retorna el numero de palitos en una pila especifica."""
        return self.state.piles[index]
    
    def get_current_player(self) -> Player:
        """Retorna el jugador que tiene el turno actual."""
        return self.state.current_player
    
    def get_total_sticks(self, piles: List[int] = None) -> int:
        """Retorna el total de palitos restantes."""
        if piles is None:
            piles = self.state.piles
        return sum(piles)
    
    def get_valid_moves(self, piles: List[int] = None) -> List[Tuple[int, int]]:
        """
        Obtiene la lista de movimientos validos.
        
        Args:
            piles: Estado de pilas a considerar. Si es None, usa el estado actual.
        
        Returns:
            Lista de tuplas (pile_index, sticks_to_remove).
        """
        if piles is None:
            piles = self.state.piles
        
        moves = []
        for pile_idx, pile_size in enumerate(piles):
            if pile_size > 0:
                max_remove = min(self.MAX_TAKE, pile_size)
                for sticks in range(self.MIN_TAKE, max_remove + 1):
                    moves.append((pile_idx, sticks))
        return moves
    
    def get_valid_moves_for_pile(self, pile_index: int, piles: List[int] = None) -> List[int]:
        """
        Obtiene los movimientos validos para una pila especifica.
        
        Args:
            pile_index: Indice de la pila.
            piles: Estado de pilas. Si es None, usa el actual.
        
        Returns:
            Lista de cantidades validas a remover.
        """
        if piles is None:
            piles = self.state.piles
        
        pile_size = piles[pile_index]
        if pile_size == 0:
            return []
        
        max_remove = min(self.MAX_TAKE, pile_size)
        return list(range(self.MIN_TAKE, max_remove + 1))
    
    def is_valid_move(self, pile_index: int, sticks: int, piles: List[int] = None) -> bool:
        """
        Verifica si un movimiento es valido.
        """
        if piles is None:
            piles = self.state.piles
        
        if pile_index < 0 or pile_index >= len(piles):
            return False
        if sticks < self.MIN_TAKE or sticks > self.MAX_TAKE:
            return False
        if sticks > piles[pile_index]:
            return False
        return True
    
    def make_move(self, pile_index: int, sticks: int) -> bool:
        """
        Ejecuta un movimiento en el juego actual.
        
        Args:
            pile_index: Indice de la pila (0, 1 o 2).
            sticks: Numero de palitos a remover (1-3).
        
        Returns:
            True si el movimiento se ejecuto exitosamente.
        """
        if not self.is_valid_move(pile_index, sticks):
            return False
        
        self.state.move_history.append((self.state.current_player, pile_index, sticks))
        self.state.piles[pile_index] -= sticks
        
        if not self.is_terminal():
            self.state.current_player = (
                Player.AGENT if self.state.current_player == Player.HUMAN 
                else Player.HUMAN
            )
        
        return True
    
    def apply_move(self, piles: List[int], pile_index: int, sticks: int) -> List[int]:
        """Aplica un movimiento a un estado sin modificar el juego actual."""
        new_piles = piles.copy()
        new_piles[pile_index] -= sticks
        return new_piles
    
    def is_terminal(self, piles: List[int] = None) -> bool:
        """Verifica si el estado es terminal."""
        if piles is None:
            piles = self.state.piles
        return sum(piles) == 0
    
    def is_game_over(self) -> bool:
        """Verifica si el juego ha terminado."""
        return self.is_terminal()
    
    def get_winner(self) -> Optional[Player]:
        """Obtiene el ganador del juego."""
        if not self.is_game_over():
            return None
        if self.state.move_history:
            return self.state.move_history[-1][0]
        return None
    
    def calculate_nim_sum(self, piles: List[int] = None) -> int:
        """
        Calcula el Nim-sum (XOR) del estado actual.
        
        El Nim-sum es 0 si y solo si la posicion es perdedora
        para el jugador que debe mover.
        """
        if piles is None:
            piles = self.state.piles
        
        nim_sum = 0
        for pile in piles:
            nim_sum ^= pile
        return nim_sum
    
    def is_winning_position(self, piles: List[int] = None) -> bool:
        """Determina si la posicion actual es ganadora para quien mueve."""
        return self.calculate_nim_sum(piles) != 0
    
    def get_optimal_move(self, piles: List[int] = None) -> Optional[Tuple[int, int]]:
        """
        Obtiene el movimiento optimo usando la estrategia de Nim-sum.
        
        Returns:
            Tupla (pile_index, sticks) o None si no hay movimiento ganador.
        """
        if piles is None:
            piles = self.state.piles
        
        nim_sum = self.calculate_nim_sum(piles)
        
        if nim_sum == 0:
            return None
        
        for pile_idx, pile_size in enumerate(piles):
            if pile_size == 0:
                continue
            
            target = pile_size ^ nim_sum
            
            if target < pile_size:
                sticks_to_remove = pile_size - target
                if self.MIN_TAKE <= sticks_to_remove <= self.MAX_TAKE:
                    return (pile_idx, sticks_to_remove)
        
        return None
    
    def __str__(self) -> str:
        """Representacion en cadena del estado del juego."""
        lines = ["Estado del juego de Nim:"]
        for i, pile in enumerate(self.state.piles):
            lines.append(f"  Fila {i + 1}: {'|' * pile} ({pile})")
        lines.append(f"Nim-sum: {self.calculate_nim_sum()}")
        lines.append(f"Turno: {self.state.current_player.name}")
        if self.is_game_over():
            winner = self.get_winner()
            lines.append(f"Ganador: {winner.name if winner else 'N/A'}")
        return "\n".join(lines)
