import sys

import pygame

from src.config import *
from src.game_logic.board import Board
from src.gui.renderer import Renderer


def main_game_loop():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tres en Raya - Dos Jugadores")
    clock = pygame.time.Clock()

    board = Board()
    renderer = Renderer(screen)

    # --- Bucle Principal del Juego ---
    running = True
    while running:
        # 1. Manejo de Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Evento de clic del ratón
            if event.type == pygame.MOUSEBUTTONDOWN and not board.game_over:
                mouseX, mouseY = event.pos
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE
                board.make_move(clicked_row, clicked_col)

            # Evento de teclado para reiniciar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board.reset()

        # 2. Dibujar todo en la pantalla
        renderer.draw_grid()
        renderer.draw_symbols(board.board)

        if board.game_over:
            renderer.draw_win_line(board)
            renderer.draw_game_over_text(board)

        # 3. Actualizar la pantalla
        pygame.display.update()
        clock.tick(FPS)

    # --- Salir del juego ---
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main_game_loop()
