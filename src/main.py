"""
Punto de entrada principal para el juego de Nim con Minimax AI.
"""

import sys
from graphics import run_gui


def main():
    """
    Funcion principal que inicia el juego de Nim.
    
    Returns:
        int: Codigo de salida de la aplicacion.
    """
    return run_gui()


if __name__ == "__main__":
    sys.exit(main())
