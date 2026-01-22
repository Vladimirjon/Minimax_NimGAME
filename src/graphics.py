"""
Interfaz grafica mejorada para el juego de Nim usando PyQt6.

Caracteristicas:
- Visualizacion 3D de los palitos
- Seleccion de fila para remover palitos
- Interfaz limpia centrada en el juego
"""

import sys
from typing import Optional, List
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QComboBox, QMessageBox,
    QGraphicsDropShadowEffect, QButtonGroup
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import (
    QPainter, QColor, QBrush, QPen, QFont, QLinearGradient,
    QRadialGradient, QPainterPath
)

from nim import NimGame, Player
from game_agent import NimGameAgent, Difficulty


class Stick3DWidget(QWidget):
    """
    Widget que representa un palito con efecto 3D.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_active = True
        self.is_highlighted = False
        self.is_selected_for_removal = False
        self.setMinimumSize(28, 90)
        self.setMaximumSize(35, 110)
    
    def set_active(self, active: bool) -> None:
        """Establece si el palito esta activo."""
        self.is_active = active
        self.update()
    
    def set_highlighted(self, highlighted: bool) -> None:
        """Establece si el palito esta resaltado (hover)."""
        self.is_highlighted = highlighted
        self.update()
    
    def set_selected_for_removal(self, selected: bool) -> None:
        """Establece si el palito sera removido."""
        self.is_selected_for_removal = selected
        self.update()
    
    def paintEvent(self, event):
        """Dibuja el palito con efecto 3D."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        center_x = rect.width() // 2
        stick_width = 18
        stick_height = rect.height() - 15
        x = center_x - stick_width // 2
        y = 8
        
        if not self.is_active:
            # Palito removido - mostrar sombra tenue
            painter.setPen(QPen(QColor(180, 180, 180, 100), 1, Qt.PenStyle.DotLine))
            painter.drawLine(center_x, y + 10, center_x, y + stick_height - 10)
            return
        
        # Colores base segun estado
        if self.is_selected_for_removal:
            base_color = QColor(231, 76, 60)  # Rojo
            highlight_color = QColor(255, 120, 100)
            shadow_color = QColor(180, 50, 40)
        elif self.is_highlighted:
            base_color = QColor(241, 196, 15)  # Amarillo
            highlight_color = QColor(255, 230, 100)
            shadow_color = QColor(180, 140, 10)
        else:
            base_color = QColor(139, 90, 43)  # Marron madera
            highlight_color = QColor(205, 150, 100)
            shadow_color = QColor(90, 55, 25)
        
        # Sombra del palito
        shadow_path = QPainterPath()
        shadow_path.addRoundedRect(x + 3, y + 3, stick_width, stick_height, 4, 4)
        painter.fillPath(shadow_path, QColor(0, 0, 0, 60))
        
        # Cuerpo principal del palito con gradiente
        body_gradient = QLinearGradient(x, 0, x + stick_width, 0)
        body_gradient.setColorAt(0, shadow_color)
        body_gradient.setColorAt(0.3, base_color)
        body_gradient.setColorAt(0.5, highlight_color)
        body_gradient.setColorAt(0.7, base_color)
        body_gradient.setColorAt(1, shadow_color)
        
        body_path = QPainterPath()
        body_path.addRoundedRect(x, y, stick_width, stick_height, 4, 4)
        painter.fillPath(body_path, QBrush(body_gradient))
        
        # Borde
        painter.setPen(QPen(shadow_color.darker(130), 1))
        painter.drawRoundedRect(x, y, stick_width, stick_height, 4, 4)
        
        # Lineas de textura de madera
        painter.setPen(QPen(shadow_color.darker(110), 1, Qt.PenStyle.SolidLine))
        for i in range(3):
            line_y = y + 20 + i * 25
            if line_y < y + stick_height - 10:
                painter.drawLine(x + 4, line_y, x + stick_width - 4, line_y)
        
        # Brillo superior
        shine_gradient = QLinearGradient(x, y, x, y + 20)
        shine_gradient.setColorAt(0, QColor(255, 255, 255, 80))
        shine_gradient.setColorAt(1, QColor(255, 255, 255, 0))
        
        shine_path = QPainterPath()
        shine_path.addRoundedRect(x + 2, y + 2, stick_width - 4, 15, 3, 3)
        painter.fillPath(shine_path, QBrush(shine_gradient))


class PileWidget(QWidget):
    """
    Widget que representa una fila de palitos.
    """
    
    def __init__(self, pile_index: int, initial_count: int, parent=None):
        super().__init__(parent)
        self.pile_index = pile_index
        self.initial_count = initial_count
        self.current_count = initial_count
        self.is_selected = False
        self.sticks: List[Stick3DWidget] = []
        self.highlighted_count = 0
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz de la fila."""
        layout = QHBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        for _ in range(self.initial_count):
            stick = Stick3DWidget()
            self.sticks.append(stick)
            layout.addWidget(stick)
    
    def update_count(self, count: int) -> None:
        """Actualiza el numero de palitos visibles."""
        self.current_count = count
        for i, stick in enumerate(self.sticks):
            stick.set_active(i < count)
            stick.set_selected_for_removal(False)
            stick.set_highlighted(False)
        self.highlighted_count = 0
    
    def set_selected(self, selected: bool) -> None:
        """Establece si esta fila esta seleccionada."""
        self.is_selected = selected
        if not selected:
            self.clear_highlights()
    
    def highlight_sticks(self, count: int) -> None:
        """Resalta los palitos que seran removidos."""
        self.highlighted_count = min(count, self.current_count)
        for i, stick in enumerate(self.sticks):
            if stick.is_active:
                # Resaltar desde el final
                active_index = sum(1 for s in self.sticks[:i+1] if s.is_active)
                should_highlight = active_index > (self.current_count - self.highlighted_count)
                stick.set_selected_for_removal(should_highlight)
    
    def clear_highlights(self) -> None:
        """Limpia todos los resaltados."""
        self.highlighted_count = 0
        for stick in self.sticks:
            stick.set_selected_for_removal(False)
            stick.set_highlighted(False)
    
    def get_highlighted_count(self) -> int:
        """Retorna el numero de palitos resaltados."""
        return self.highlighted_count


class GameBoardWidget(QWidget):
    """
    Widget principal del tablero de juego con efecto 3D.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.piles: List[PileWidget] = []
        self.selected_pile: Optional[int] = None
        self.on_pile_selected = None  # Callback
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz del tablero."""
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Crear las 3 filas con configuracion [3, 5, 7]
        pile_configs = [3, 5, 7]
        
        for i, count in enumerate(pile_configs):
            # Contenedor de fila con boton
            row_container = QWidget()
            row_layout = QHBoxLayout(row_container)
            row_layout.setContentsMargins(0, 0, 0, 0)
            
            # Etiqueta de fila
            label = QLabel(f"Fila {i + 1}")
            label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: bold;
                    color: #ecf0f1;
                    min-width: 60px;
                }
            """)
            row_layout.addWidget(label)
            
            # Pila de palitos
            pile = PileWidget(i, count)
            pile.setStyleSheet("""
                QWidget {
                    background-color: rgba(52, 73, 94, 0.6);
                    border-radius: 10px;
                }
            """)
            self.piles.append(pile)
            row_layout.addWidget(pile, stretch=1)
            
            # Boton de seleccion
            select_btn = QPushButton("Seleccionar")
            select_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: bold;
                    min-width: 100px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #21618c;
                }
                QPushButton:disabled {
                    background-color: #7f8c8d;
                }
            """)
            select_btn.clicked.connect(lambda checked, idx=i: self._on_pile_clicked(idx))
            row_layout.addWidget(select_btn)
            
            layout.addWidget(row_container)
        
        layout.addStretch()
    
    def _on_pile_clicked(self, pile_index: int) -> None:
        """Maneja el clic en una fila."""
        # Deseleccionar anterior
        if self.selected_pile is not None:
            self.piles[self.selected_pile].set_selected(False)
        
        # Verificar si la fila tiene palitos
        if self.piles[pile_index].current_count > 0:
            self.selected_pile = pile_index
            self.piles[pile_index].set_selected(True)
            
            if self.on_pile_selected:
                self.on_pile_selected(pile_index)
    
    def update_piles(self, pile_counts: List[int]) -> None:
        """Actualiza el estado de todas las pilas."""
        for i, count in enumerate(pile_counts):
            self.piles[i].update_count(count)
        
        # Si la pila seleccionada esta vacia, deseleccionar
        if self.selected_pile is not None:
            if pile_counts[self.selected_pile] == 0:
                self.selected_pile = None
    
    def highlight_removal(self, pile_index: int, count: int) -> None:
        """Resalta los palitos que seran removidos."""
        if 0 <= pile_index < len(self.piles):
            self.piles[pile_index].highlight_sticks(count)
    
    def clear_selection(self) -> None:
        """Limpia la seleccion actual."""
        if self.selected_pile is not None:
            self.piles[self.selected_pile].set_selected(False)
            self.piles[self.selected_pile].clear_highlights()
        self.selected_pile = None
    
    def get_selected_pile(self) -> Optional[int]:
        """Retorna el indice de la pila seleccionada."""
        return self.selected_pile
    
    def paintEvent(self, event):
        """Dibuja el fondo del tablero con efecto 3D."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Fondo con gradiente
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(44, 62, 80))
        gradient.setColorAt(1, QColor(30, 40, 50))
        
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 20, 20)
        painter.fillPath(path, QBrush(gradient))
        
        # Borde con efecto de profundidad
        painter.setPen(QPen(QColor(52, 73, 94), 3))
        painter.drawRoundedRect(2, 2, self.width() - 4, self.height() - 4, 18, 18)


class ControlPanel(QWidget):
    """
    Panel de control simplificado.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.on_remove_clicked = None
        self.on_new_game = None
        self.on_difficulty_changed = None
        self.remove_buttons: List[QPushButton] = []
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz del panel."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Selector de dificultad
        diff_layout = QHBoxLayout()
        diff_label = QLabel("Dificultad:")
        diff_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        diff_layout.addWidget(diff_label)
        
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Facil", "Medio", "Dificil", "Optimo"])
        self.difficulty_combo.setCurrentIndex(3)  # Optimo por defecto
        self.difficulty_combo.setStyleSheet("""
            QComboBox {
                background-color: #34495e;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 14px;
                min-width: 120px;
            }
            QComboBox:hover {
                background-color: #3d566e;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid white;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #34495e;
                color: white;
                selection-background-color: #2980b9;
            }
        """)
        self.difficulty_combo.currentTextChanged.connect(self._on_difficulty_changed)
        diff_layout.addWidget(self.difficulty_combo)
        layout.addLayout(diff_layout)
        
        # Separador
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #bdc3c7;")
        layout.addWidget(line)
        
        # Instruccion
        instruction = QLabel("Selecciona una fila y elige\ncuantos palitos remover:")
        instruction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction.setStyleSheet("font-size: 13px; color: #7f8c8d;")
        layout.addWidget(instruction)
        
        # Botones de cantidad
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        for i in range(1, 4):
            btn = QPushButton(f"Quitar {i}")
            btn.setEnabled(False)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 8px;
                    font-size: 13px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #229954;
                }
                QPushButton:pressed {
                    background-color: #1e8449;
                }
                QPushButton:disabled {
                    background-color: #95a5a6;
                    color: #bdc3c7;
                }
            """)
            btn.clicked.connect(lambda checked, count=i: self._on_remove(count))
            self.remove_buttons.append(btn)
            buttons_layout.addWidget(btn)
        
        layout.addLayout(buttons_layout)
        
        # Boton nuevo juego
        self.new_game_btn = QPushButton("Nuevo Juego")
        self.new_game_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:pressed {
                background-color: #7d3c98;
            }
        """)
        self.new_game_btn.clicked.connect(self._on_new_game)
        layout.addWidget(self.new_game_btn)
        
        layout.addStretch()
    
    def _on_remove(self, count: int) -> None:
        """Maneja el clic en boton de remover."""
        if self.on_remove_clicked:
            self.on_remove_clicked(count)
    
    def _on_new_game(self) -> None:
        """Maneja el clic en nuevo juego."""
        if self.on_new_game:
            self.on_new_game()
    
    def _on_difficulty_changed(self, text: str) -> None:
        """Maneja el cambio de dificultad."""
        if self.on_difficulty_changed:
            self.on_difficulty_changed(text)
    
    def update_buttons(self, max_remove: int, pile_selected: bool) -> None:
        """Actualiza el estado de los botones."""
        for i, btn in enumerate(self.remove_buttons):
            count = i + 1
            enabled = pile_selected and count <= max_remove
            btn.setEnabled(enabled)
    
    def set_enabled(self, enabled: bool) -> None:
        """Habilita o deshabilita los controles."""
        for btn in self.remove_buttons:
            if enabled:
                # Se actualizara con update_buttons
                pass
            else:
                btn.setEnabled(False)


class NimMainWindow(QMainWindow):
    """
    Ventana principal del juego de Nim.
    """
    
    def __init__(self):
        super().__init__()
        self.game = NimGame()
        self.agent = NimGameAgent(self.game, difficulty='optimal')
        self.is_player_turn = True
        
        self._setup_ui()
        self._update_display()
    
    def _setup_ui(self):
        """Configura la interfaz principal."""
        self.setWindowTitle("Nim Game - Minimax AI")
        self.setMinimumSize(900, 650)
        self.setStyleSheet("background-color: #ecf0f1;")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Panel izquierdo (juego)
        left_panel = QVBoxLayout()
        
        # Titulo
        title = QLabel("NIM")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 48px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
            font-family: 'Arial Black', sans-serif;
        """)
        left_panel.addWidget(title)
        
        # Tablero
        self.board = GameBoardWidget()
        self.board.on_pile_selected = self._on_pile_selected
        left_panel.addWidget(self.board, stretch=1)
        
        # Indicador de turno
        self.turn_label = QLabel("Tu turno")
        self.turn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turn_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #27ae60;
            padding: 15px;
        """)
        left_panel.addWidget(self.turn_label)
        
        main_layout.addLayout(left_panel, stretch=2)
        
        # Panel derecho (controles)
        self.controls = ControlPanel()
        self.controls.on_remove_clicked = self._on_remove_sticks
        self.controls.on_new_game = self._new_game
        self.controls.on_difficulty_changed = self._on_difficulty_changed
        self.controls.setMaximumWidth(280)
        self.controls.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
            }
        """)
        
        # Agregar sombra al panel
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 5)
        self.controls.setGraphicsEffect(shadow)
        
        main_layout.addWidget(self.controls)
    
    def _update_display(self) -> None:
        """Actualiza toda la interfaz."""
        piles = self.game.get_piles()
        self.board.update_piles(piles)
        
        # Actualizar botones segun pila seleccionada
        selected = self.board.get_selected_pile()
        if selected is not None and piles[selected] > 0:
            max_remove = min(3, piles[selected])
            self.controls.update_buttons(max_remove, True)
        else:
            self.controls.update_buttons(0, False)
        
        # Verificar fin del juego
        if self.game.is_game_over():
            winner = self.game.get_winner()
            if winner == Player.HUMAN:
                self._show_game_over("Victoria", "Ganaste!")
                self.turn_label.setText("Ganaste!")
                self.turn_label.setStyleSheet("""
                    font-size: 24px;
                    font-weight: bold;
                    color: #27ae60;
                    padding: 15px;
                """)
            else:
                self._show_game_over("Derrota", "La IA gano!")
                self.turn_label.setText("Perdiste!")
                self.turn_label.setStyleSheet("""
                    font-size: 24px;
                    font-weight: bold;
                    color: #e74c3c;
                    padding: 15px;
                """)
            self.controls.set_enabled(False)
    
    def _on_pile_selected(self, pile_index: int) -> None:
        """Maneja la seleccion de una fila."""
        if not self.is_player_turn or self.game.is_game_over():
            return
        
        piles = self.game.get_piles()
        max_remove = min(3, piles[pile_index])
        self.controls.update_buttons(max_remove, True)
    
    def _on_remove_sticks(self, count: int) -> None:
        """Maneja la accion de remover palitos."""
        if not self.is_player_turn or self.game.is_game_over():
            return
        
        selected = self.board.get_selected_pile()
        if selected is None:
            return
        
        # Ejecutar movimiento
        if self.game.make_move(selected, count):
            self.board.clear_selection()
            self._update_display()
            
            if not self.game.is_game_over():
                self.is_player_turn = False
                self.controls.set_enabled(False)
                self.turn_label.setText("Turno de la IA...")
                self.turn_label.setStyleSheet("""
                    font-size: 24px;
                    font-weight: bold;
                    color: #e74c3c;
                    padding: 15px;
                """)
                
                QTimer.singleShot(800, self._agent_move)
    
    def _agent_move(self) -> None:
        """Ejecuta el movimiento del agente."""
        if self.game.is_game_over():
            return
        
        move = self.agent.get_move()
        
        if move is not None:
            pile_idx, sticks = move
            
            # Mostrar que fila va a afectar
            self.board.highlight_removal(pile_idx, sticks)
            
            # Esperar un momento para que se vea la seleccion
            QTimer.singleShot(500, lambda: self._execute_agent_move(pile_idx, sticks))
    
    def _execute_agent_move(self, pile_idx: int, sticks: int) -> None:
        """Ejecuta el movimiento del agente despues de la animacion."""
        self.game.make_move(pile_idx, sticks)
        self.board.clear_selection()
        self._update_display()
        
        if not self.game.is_game_over():
            self.is_player_turn = True
            self.controls.set_enabled(True)
            self.turn_label.setText("Tu turno")
            self.turn_label.setStyleSheet("""
                font-size: 24px;
                font-weight: bold;
                color: #27ae60;
                padding: 15px;
            """)
    
    def _new_game(self) -> None:
        """Inicia un nuevo juego."""
        self.game.reset()
        self.board.clear_selection()
        self.is_player_turn = True
        self.controls.set_enabled(True)
        self.turn_label.setText("Tu turno")
        self.turn_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #27ae60;
            padding: 15px;
        """)
        self._update_display()
    
    def _on_difficulty_changed(self, difficulty: str) -> None:
        """Maneja el cambio de dificultad."""
        self.agent.set_difficulty(difficulty)
    
    def _show_game_over(self, title: str, message: str) -> None:
        """Muestra el dialogo de fin de juego."""
        # Notificar al agente
        winner = self.game.get_winner()
        self.agent.notify_game_end(winner == Player.AGENT)


def run_gui():
    """Funcion principal para ejecutar la interfaz grafica."""
    app = QApplication(sys.argv)
    
    # Configurar fuente predeterminada
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = NimMainWindow()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(run_gui())
