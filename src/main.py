import sys
import time
from enum import Enum

import pygame

# Asumiendo que estos módulos existen según tu código original
from src.ai.minimax import find_best_move_alpha_beta, find_best_move_bruteforce
from src.config import *
from src.game_logic.board import Board
from src.gui.renderer import Renderer


# --- Enums y Constantes ---
class GameState(Enum):
    MENU = 0
    AI_SELECTION = 1
    PLAYING = 2


class PlayerType:
    HUMAN = "HUMAN"
    AI_SLOW = "AI_SLOW"
    AI_FAST = "AI_FAST"


class GameController:
    def __init__(self):
        # Inicialización de Pygame
        pygame.display.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Comparador de IA: Minimax vs Alfa-Beta")
        self.clock = pygame.time.Clock()

        # Componentes del juego
        self.board = Board()
        self.renderer = Renderer(self.screen)

        # Estado inicial
        self.state = GameState.MENU
        self.running = True

        # Variables de configuración de partida
        self.player_types = [PlayerType.HUMAN, PlayerType.HUMAN]
        self.ai_speed_selected = None  # Temp variable para el submenú
        self.last_graph_data = []
        self.waiting_for_step = False

        # Configuración de Menús
        self.menu_options = [
            "Humano vs Humano",
            "Humano vs IA (Lenta - Minimax)",
            "Humano vs IA (Rápida - AlfaBeta)",
            # "IA Lenta vs IA Rápida (¡Observa!)"
        ]
        self.menu_selection = 0

        self.start_options = ["Humano Inicia", "IA Inicia"]
        self.start_selection = 0

        self.menu_rects = []

    def run(self):
        """Bucle principal del juego"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    # --- Manejo de Eventos ---
    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return

            if self.state == GameState.MENU:
                self._handle_menu_input(event, self.menu_options, is_main_menu=True)

            elif self.state == GameState.AI_SELECTION:
                self._handle_menu_input(event, self.start_options, is_main_menu=False)

            elif self.state == GameState.PLAYING:
                self._handle_playing_input(event)

    def _handle_menu_input(self, event, options_list, is_main_menu):
        """Maneja input para menús (teclado y mouse) de forma genérica"""
        selection_attr = "menu_selection" if is_main_menu else "start_selection"
        current_selection = getattr(self, selection_attr)

        # Teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                setattr(
                    self, selection_attr, (current_selection - 1) % len(options_list)
                )
            elif event.key == pygame.K_DOWN:
                setattr(
                    self, selection_attr, (current_selection + 1) % len(options_list)
                )
            elif event.key == pygame.K_RETURN:
                if is_main_menu:
                    self._confirm_main_menu_selection()
                else:
                    self._confirm_ai_selection()
            elif event.key == pygame.K_ESCAPE and not is_main_menu:
                self.state = GameState.MENU

        # Mouse
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for i, rect in enumerate(self.menu_rects):
                if rect.collidepoint(mouse_pos):
                    setattr(self, selection_attr, i)
                    if is_main_menu:
                        self._confirm_main_menu_selection()
                    else:
                        self._confirm_ai_selection()
                    break

        # Actualizar selección visual con hover del mouse (opcional pero mejora UX)
        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(self.menu_rects):
            if rect.collidepoint(mouse_pos):
                setattr(self, selection_attr, i)

    def _confirm_main_menu_selection(self):
        sel = self.menu_selection
        if sel == 0:  # H v H
            self.start_game([PlayerType.HUMAN, PlayerType.HUMAN])
        elif sel == 1:  # IA Lenta
            self.ai_speed_selected = PlayerType.AI_SLOW
            self.state = GameState.AI_SELECTION
        elif sel == 2:  # IA Rápida
            self.ai_speed_selected = PlayerType.AI_FAST
            self.state = GameState.AI_SELECTION
        elif sel == 3:  # IA v IA
            self.start_game([PlayerType.AI_SLOW, PlayerType.AI_FAST])

    def _confirm_ai_selection(self):
        p1 = PlayerType.HUMAN
        p2 = self.ai_speed_selected

        if self.start_selection == 0:  # Humano inicia
            self.start_game([p1, p2])
        else:  # IA inicia
            self.start_game([p2, p1])

    def _handle_playing_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset_board()
            elif event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU
            elif event.key == pygame.K_RETURN and self.waiting_for_step:
                self.waiting_for_step = False

        if event.type == pygame.MOUSEBUTTONDOWN and not self.board.game_over:
            current_player = self.player_types[self.board.turn - 1]
            if current_player == PlayerType.HUMAN:
                self._process_human_click(event.pos)

    def _process_human_click(self, pos):
        mouseX, mouseY = pos
        # Validación de zona de clic
        if (
            self.renderer.board_offset_x
            <= mouseX
            < self.renderer.board_offset_x + BOARD_WIDTH
            and mouseY > BOARD_OFFSET_Y
        ):
            clicked_row = (mouseY - BOARD_OFFSET_Y) // SQUARE_SIZE
            clicked_col = (mouseX - self.renderer.board_offset_x) // SQUARE_SIZE

            if 0 <= clicked_row < BOARD_ROWS and 0 <= clicked_col < BOARD_COLS:
                self.board.make_move(clicked_row, clicked_col)

    # --- Lógica de Actualización (Update) ---
    def update(self):
        if self.state == GameState.PLAYING:
            self._update_game_logic()

    def _update_game_logic(self):
        # Verificar pausa por paso a paso (AI vs AI)
        if self.waiting_for_step:
            return

        current_player = self.player_types[self.board.turn - 1]

        # Si es turno de IA y el juego no ha terminado
        if not self.board.game_over and current_player in [
            PlayerType.AI_SLOW,
            PlayerType.AI_FAST,
        ]:
            self._execute_ai_turn(current_player)

    def _execute_ai_turn(self, ai_type):
        # Pequeño hack para forzar redibujado antes de cálculo pesado
        # para que se vea la pantalla actualizada antes de que la IA piense
        self.draw()

        start_time = time.time()
        move = None

        print(f"Turno {self.board.turn} ({ai_type}): Calculando...")

        if ai_type == PlayerType.AI_SLOW:
            move, self.last_graph_data = find_best_move_bruteforce(self.board)
        elif ai_type == PlayerType.AI_FAST:
            move, self.last_graph_data = find_best_move_alpha_beta(self.board)

        print(f"Cálculo: {time.time() - start_time:.4f}s")

        if move:
            self.board.make_move(move[0], move[1])

            # Si es IA vs IA, activar pausa
            if self.player_types == [PlayerType.AI_SLOW, PlayerType.AI_FAST]:
                self.waiting_for_step = True

    # --- Dibujado (Render) ---
    def draw(self):
        if self.state == GameState.MENU:
            self.menu_rects = self.renderer.draw_menu(
                self.menu_options, self.menu_selection
            )

        elif self.state == GameState.AI_SELECTION:
            self.menu_rects = self.renderer.draw_menu(
                self.start_options, self.start_selection
            )

        elif self.state == GameState.PLAYING:
            self._draw_game_screen()

        pygame.display.update()

    def _draw_game_screen(self):
        # Configurar renderer
        is_h_vs_h = self.player_types == [PlayerType.HUMAN, PlayerType.HUMAN]
        self.renderer.set_centered(is_h_vs_h)

        should_invert = (
            len(self.player_types) == 2
            and self.player_types[1] == PlayerType.HUMAN
            and self.player_types[0] != PlayerType.HUMAN
        )
        self.renderer.set_inverted(should_invert)

        # Dibujar elementos
        self.renderer.draw_grid()
        self.renderer.draw_symbols(self.board.board)
        self.renderer.draw_decision_graph(self.last_graph_data)

        # Indicador de turno
        real_current_player = self.player_types[self.board.turn - 1]
        label = "HUMAN" if real_current_player == PlayerType.HUMAN else "IA"
        self.renderer.draw_turn_indicator(self.board.turn, label)

        # Ghost Symbol (Hover)
        current_player = self.player_types[self.board.turn - 1]
        if not self.board.game_over and current_player == PlayerType.HUMAN:
            self._draw_ghost_symbol()

        # Game Over
        if self.board.game_over:
            self.renderer.draw_win_line(self.board)
            self.renderer.draw_game_over_text(self.board)

        # Prompt "Presiona Enter" para AI vs AI
        if self.waiting_for_step:
            self._draw_step_prompt()

    def _draw_ghost_symbol(self):
        mouse_pos = pygame.mouse.get_pos()
        mouseX, mouseY = mouse_pos
        if (
            self.renderer.board_offset_x
            <= mouseX
            < self.renderer.board_offset_x + BOARD_WIDTH
            and mouseY > BOARD_OFFSET_Y
        ):
            row = (mouseY - BOARD_OFFSET_Y) // SQUARE_SIZE
            col = (mouseX - self.renderer.board_offset_x) // SQUARE_SIZE
            if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
                if self.board.is_valid_move(row, col):
                    self.renderer.draw_ghost_symbol(row, col, self.board.turn)

    def _draw_step_prompt(self):
        font = pygame.font.Font(None, 40)
        prompt = font.render(
            "Presiona ENTER para siguiente jugada...", True, (255, 255, 0)
        )
        rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        bg = rect.inflate(20, 10)
        pygame.draw.rect(self.screen, (0, 0, 0), bg)
        self.screen.blit(prompt, rect)

    # --- Helpers ---
    def start_game(self, players):
        self.player_types = players
        self.state = GameState.PLAYING
        self.reset_board()

    def reset_board(self):
        self.board = Board()
        self.last_graph_data = []
        self.waiting_for_step = False
        pygame.event.clear()


if __name__ == "__main__":
    game = GameController()
    game.run()
