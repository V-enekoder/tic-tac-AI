import pygame

from src.config import *


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, FONT_SIZE)

    def draw_grid(self):
        """Dibuja las líneas del tablero."""
        self.screen.fill(BG_COLOR)
        # Líneas horizontales
        for i in range(1, BOARD_ROWS):
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (0, i * SQUARE_SIZE),
                (WIDTH, i * SQUARE_SIZE),
                LINE_WIDTH,
            )
        # Líneas verticales
        for i in range(1, BOARD_COLS):
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (i * SQUARE_SIZE, 0),
                (i * SQUARE_SIZE, HEIGHT),
                LINE_WIDTH,
            )

    def draw_symbols(self, board_array):
        """Dibuja las X y O en el tablero."""
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2

                if board_array[row][col] == 1:
                    margin = SQUARE_SIZE // 4
                    start_desc = (center_x - margin, center_y - margin)
                    end_desc = (center_x + margin, center_y + margin)
                    start_asc = (center_x - margin, center_y + margin)
                    end_asc = (center_x + margin, center_y - margin)
                    pygame.draw.line(
                        self.screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH
                    )
                    pygame.draw.line(
                        self.screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH
                    )
                elif board_array[row][col] == 2:
                    pygame.draw.circle(
                        self.screen,
                        CIRCLE_COLOR,
                        (center_x, center_y),
                        CIRCLE_RADIUS,
                        CIRCLE_WIDTH,
                    )

    def draw_win_line(self, board):
        """Dibuja la línea que tacha la jugada ganadora."""
        if not board.win_info:
            return

        win_type, index = board.win_info

        if win_type == "row":
            y_pos = index * SQUARE_SIZE + SQUARE_SIZE // 2
            start_pos = (15, y_pos)
            end_pos = (WIDTH - 15, y_pos)
        elif win_type == "col":
            x_pos = index * SQUARE_SIZE + SQUARE_SIZE // 2
            start_pos = (x_pos, 15)
            end_pos = (x_pos, HEIGHT - 15)
        elif win_type == "diag":
            if index == 1:  # Descendente
                start_pos = (15, 15)
                end_pos = (WIDTH - 15, HEIGHT - 15)
            else:  # Ascendente
                start_pos = (15, HEIGHT - 15)
                end_pos = (WIDTH - 15, 15)

        pygame.draw.line(self.screen, WIN_LINE_COLOR, start_pos, end_pos, LINE_WIDTH)

    def draw_game_over_text(self, board):
        """Muestra un mensaje al final del juego."""
        if not board.game_over:
            return

        if board.winner == 0:
            text = "¡Es un empate!"
        else:
            text = f"¡Jugador {board.winner} gana!"

        rendered_text = self.font.render(text, True, FONT_COLOR)
        text_rect = rendered_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

        restart_text = self.font.render("Pulsa 'R' para reiniciar", True, FONT_COLOR)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

        # Fondo semi-transparente para el texto
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))

        self.screen.blit(rendered_text, text_rect)
        self.screen.blit(restart_text, restart_rect)
