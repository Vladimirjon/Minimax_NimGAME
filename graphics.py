"""
graphics.py - Pygame UI for Nim Game

This module provides a graphical user interface for the Nim game using Pygame.
It displays:
- A left-aligned pyramid of sticks (3, 5, 7 rows)
- Current game state (sticks remaining)
- Agent's decision statistics
- Controls for human player
"""

import pygame
from typing import Optional, Tuple
from nim import NimGame, get_pyramid_representation
from minimax import MinimaxStats


# Color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)  # Stick color
DARK_BROWN = (101, 67, 33)  # Stick shadow
GREEN = (34, 139, 34)  # Button/highlight color
DARK_GREEN = (0, 100, 0)
RED = (220, 20, 60)  # Error/warning color
BLUE = (70, 130, 180)  # Info color
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
BACKGROUND = (245, 245, 220)  # Beige background


class NimGraphics:
    """
    Pygame-based graphical interface for the Nim game.
    
    Displays a left-aligned pyramid visualization of the game state
    and provides controls for human players.
    """
    
    # Screen dimensions
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    
    # Stick dimensions
    STICK_WIDTH = 12
    STICK_HEIGHT = 60
    STICK_SPACING = 20
    
    # Pyramid layout
    PYRAMID_ROWS = [3, 5, 7]  # Sticks per row (top to bottom)
    PYRAMID_TOP_Y = 150
    PYRAMID_LEFT_X = 100
    ROW_SPACING = 80
    
    # Timing
    FPS = 60  # Target frames per second
    
    def __init__(self):
        """Initialize the Pygame graphics system."""
        pygame.init()
        pygame.display.set_caption("Nim Game - Minimax AI")
        
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 28)
        
        # Game state for display
        self.message = ""
        self.message_color = BLACK
        self.last_agent_stats: Optional[MinimaxStats] = None
        self.last_agent_action: Optional[int] = None
        self.show_invalid_move = False
        self.invalid_move_timer = 0
    
    def draw_stick(self, x: int, y: int, highlighted: bool = False):
        """
        Draw a single stick at the given position.
        
        Args:
            x: X coordinate of stick center
            y: Y coordinate of stick top
            highlighted: Whether to highlight the stick
        """
        color = GREEN if highlighted else BROWN
        shadow_color = DARK_GREEN if highlighted else DARK_BROWN
        
        # Draw shadow
        shadow_rect = pygame.Rect(
            x - self.STICK_WIDTH // 2 + 3,
            y + 3,
            self.STICK_WIDTH,
            self.STICK_HEIGHT
        )
        pygame.draw.rect(self.screen, shadow_color, shadow_rect, border_radius=3)
        
        # Draw stick
        stick_rect = pygame.Rect(
            x - self.STICK_WIDTH // 2,
            y,
            self.STICK_WIDTH,
            self.STICK_HEIGHT
        )
        pygame.draw.rect(self.screen, color, stick_rect, border_radius=3)
    
    def draw_pyramid(self, n_remaining: int):
        """
        Draw the pyramid visualization of sticks.
        
        Args:
            n_remaining: Number of sticks remaining in the game
        """
        row1, row2, row3 = get_pyramid_representation(n_remaining)
        rows = [row1, row2, row3]
        full_rows = [3, 5, 7]
        
        for row_idx, (current_count, full_count) in enumerate(zip(rows, full_rows)):
            y = self.PYRAMID_TOP_Y + row_idx * self.ROW_SPACING
            
            for stick_idx in range(full_count):
                x = self.PYRAMID_LEFT_X + stick_idx * self.STICK_SPACING
                
                if stick_idx < current_count:
                    # Draw visible stick
                    self.draw_stick(x, y)
                else:
                    # Draw placeholder (ghost stick)
                    ghost_rect = pygame.Rect(
                        x - self.STICK_WIDTH // 2,
                        y,
                        self.STICK_WIDTH,
                        self.STICK_HEIGHT
                    )
                    pygame.draw.rect(self.screen, LIGHT_GRAY, ghost_rect, 
                                   border_radius=3, width=1)
    
    def draw_game_info(self, game: NimGame):
        """
        Draw game information (sticks remaining, current player, etc.)
        
        Args:
            game: Current NimGame state
        """
        # Draw sticks remaining
        text = f"Sticks Remaining: {game.n_remaining}"
        text_surface = self.font_large.render(text, True, BLACK)
        self.screen.blit(text_surface, (400, 100))
        
        # Draw current player
        if game.is_terminal():
            winner = game.winner()
            if winner == NimGame.PLAYER_MAX:
                player_text = "AGENT WINS!"
                color = GREEN
            else:
                player_text = "HUMAN WINS!"
                color = BLUE
        else:
            if game.current_player == NimGame.PLAYER_MAX:
                player_text = "Agent's Turn"
                color = GREEN
            else:
                player_text = "Your Turn (Press 1, 2, or 3)"
                color = BLUE
        
        text_surface = self.font_medium.render(player_text, True, color)
        self.screen.blit(text_surface, (400, 150))
    
    def draw_controls_help(self):
        """Draw the controls help section."""
        y_start = 450
        
        title = self.font_medium.render("Controls:", True, BLACK)
        self.screen.blit(title, (50, y_start))
        
        controls = [
            "Press 1 - Remove 1 stick",
            "Press 2 - Remove 2 sticks",
            "Press 3 - Remove 3 sticks",
            "Press R - New Game",
            "Press Q - Quit"
        ]
        
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, GRAY)
            self.screen.blit(text, (50, y_start + 35 + i * 25))
    
    def draw_agent_stats(self):
        """Draw the agent's decision statistics."""
        if self.last_agent_stats is None:
            return
        
        y_start = 400
        x_start = 400
        
        title = self.font_medium.render("Agent Stats:", True, GREEN)
        self.screen.blit(title, (x_start, y_start))
        
        stats_lines = [
            f"Last Move: Take {self.last_agent_action}" if self.last_agent_action else "",
            f"Nodes Evaluated: {self.last_agent_stats.nodes_evaluated}",
            f"Max Depth: {self.last_agent_stats.max_depth_reached}",
            f"Time: {self.last_agent_stats.elapsed_time_ms:.3f} ms"
        ]
        
        for i, line in enumerate(stats_lines):
            if line:
                text = self.font_small.render(line, True, DARK_GREEN)
                self.screen.blit(text, (x_start, y_start + 35 + i * 25))
    
    def draw_message(self):
        """Draw the current message (if any)."""
        if self.message:
            text_surface = self.font_medium.render(self.message, True, self.message_color)
            self.screen.blit(text_surface, (400, 200))
        
        if self.show_invalid_move:
            text = self.font_medium.render("Invalid move!", True, RED)
            self.screen.blit(text, (400, 250))
    
    def draw(self, game: NimGame):
        """
        Draw the complete game screen.
        
        Args:
            game: Current NimGame state
        """
        self.screen.fill(BACKGROUND)
        
        # Draw title
        title = self.font_large.render("NIM GAME", True, BLACK)
        self.screen.blit(title, (350, 30))
        
        # Draw pyramid
        self.draw_pyramid(game.n_remaining)
        
        # Draw game info
        self.draw_game_info(game)
        
        # Draw controls
        self.draw_controls_help()
        
        # Draw agent stats
        self.draw_agent_stats()
        
        # Draw messages
        self.draw_message()
        
        # Update invalid move timer
        if self.show_invalid_move:
            self.invalid_move_timer -= 1
            if self.invalid_move_timer <= 0:
                self.show_invalid_move = False
        
        pygame.display.flip()
    
    def set_message(self, message: str, color: Tuple[int, int, int] = BLACK):
        """Set a message to display on screen."""
        self.message = message
        self.message_color = color
    
    def clear_message(self):
        """Clear the current message."""
        self.message = ""
    
    def show_invalid_move_feedback(self):
        """Show invalid move feedback for a short time (approximately 1 second)."""
        self.show_invalid_move = True
        self.invalid_move_timer = self.FPS  # Duration in frames (1 second at default FPS)
    
    def update_agent_stats(self, action: int, stats: MinimaxStats):
        """
        Update the displayed agent statistics.
        
        Args:
            action: The action the agent took
            stats: The minimax statistics from the decision
        """
        self.last_agent_action = action
        self.last_agent_stats = stats
    
    def get_human_action(self) -> Optional[int]:
        """
        Check for human input and return the action if valid key pressed.
        
        Returns:
            Action (1, 2, or 3) if corresponding key pressed, None otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2
                elif event.key == pygame.K_3:
                    return 3
                elif event.key == pygame.K_r:
                    return 'reset'
                elif event.key == pygame.K_q:
                    return 'quit'
        
        return None
    
    def wait_for_key(self, timeout_ms: int = 0) -> Optional[str]:
        """
        Wait for a key press.
        
        Args:
            timeout_ms: Maximum time to wait (0 = indefinite)
            
        Returns:
            Key name or None if timeout
        """
        start_time = pygame.time.get_ticks()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN:
                    return event.key
            
            if timeout_ms > 0:
                if pygame.time.get_ticks() - start_time > timeout_ms:
                    return None
            
            self.clock.tick(60)
    
    def tick(self, fps: int = 60):
        """Advance the clock by one frame."""
        self.clock.tick(fps)
    
    def quit(self):
        """Clean up Pygame resources."""
        pygame.quit()


def run_demo():
    """Run a simple demo of the graphics module."""
    graphics = NimGraphics()
    game = NimGame()
    
    running = True
    while running:
        action = graphics.get_human_action()
        
        if action == 'quit':
            running = False
        elif action == 'reset':
            game = NimGame()
            graphics.clear_message()
        elif action in [1, 2, 3]:
            if not game.is_terminal():
                legal = game.get_legal_actions()
                if action in legal:
                    game.apply_action_inplace(action)
                else:
                    graphics.show_invalid_move_feedback()
        
        graphics.draw(game)
        graphics.tick()
    
    graphics.quit()


if __name__ == "__main__":
    run_demo()
