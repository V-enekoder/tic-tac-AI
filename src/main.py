import sys
import time

import pygame

from src.ai.minimax import find_best_move_alpha_beta, find_best_move_bruteforce
from src.config import *
from src.game_logic.board import Board
from src.gui.renderer import Renderer

HUMAN = "HUMAN"
AI_SLOW = "AI_SLOW"
AI_FAST = "AI_FAST"


def main_game_loop():
    # --- Inicialización ---
    pygame.display.init()
    pygame.font.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Comparador de IA: Minimax vs Alfa-Beta")
    clock = pygame.time.Clock()

    board = Board()
    renderer = Renderer(screen)

    # --- Variables de Estado y Menú Ampliado ---
    game_state = "MENU"
    player_types = None

    menu_options = [
        "Humano vs Humano",
        "Humano vs IA (Lenta - Minimax)",
        "Humano vs IA (Rápida - AlfaBeta)",
        "IA Lenta vs IA Rápida (¡Observa!)",
    ]
    selected_option = 0
    running = True
    while running:
        if game_state == "MENU":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:
                            player_types = [HUMAN, HUMAN]
                        elif selected_option == 1:
                            player_types = [HUMAN, AI_SLOW]
                        elif selected_option == 2:
                            player_types = [HUMAN, AI_FAST]
                        elif selected_option == 3:
                            player_types = [AI_SLOW, AI_FAST]

                        board.reset()
                        game_state = "PLAYING"

            renderer.draw_menu(menu_options, selected_option)

        # --- Lógica de la Partida ---
        elif game_state == "PLAYING":
            current_player_type = player_types[board.turn - 1]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        board.reset()
                    if event.key == pygame.K_ESCAPE:
                        game_state = "MENU"

                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and not board.game_over
                    and current_player_type == HUMAN
                ):
                    mouseX, mouseY = event.pos
                    clicked_row, clicked_col = (
                        mouseY // SQUARE_SIZE,
                        mouseX // SQUARE_SIZE,
                    )
                    board.make_move(clicked_row, clicked_col)

            # Lógica para llamar a la IA correcta
            if not board.game_over and current_player_type in [AI_SLOW, AI_FAST]:
                start_time = time.time()
                move = None

                if current_player_type == AI_SLOW:
                    print(f"Turno {board.turn} (IA Lenta): Calculando movimiento...")
                    move = find_best_move_bruteforce(board)

                elif current_player_type == AI_FAST:
                    print(f"Turno {board.turn} (IA Rápida): Calculando movimiento...")
                    move = find_best_move_alpha_beta(board)

                end_time = time.time()
                print(f"Cálculo completado en {end_time - start_time:.4f} segundos.")

                if move:
                    board.make_move(move[0], move[1])

            # Dibujado
            renderer.draw_grid()
            renderer.draw_symbols(board.board)
            if board.game_over:
                renderer.draw_win_line(board)
                renderer.draw_game_over_text(board)

        # --- Actualización de Pantalla ---
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main_game_loop()
