# src/ai/minimax.py

import math
from copy import deepcopy
from typing import List, Tuple

from src.game_logic.board import Board

AI_PLAYER = 2
HUMAN_PLAYER = 1


def minimax_bruteforce(board: Board, depth: int, is_maximizing: bool) -> int:
    """Versión original y no optimizada de Minimax."""
    if board.winner == AI_PLAYER:
        return 1
    if board.winner == HUMAN_PLAYER:
        return -1
    if board.is_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in board.get_available_moves():
            temp_board = deepcopy(board)
            temp_board.make_move(move[0], move[1])
            score = minimax_bruteforce(temp_board, depth + 1, False)
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in board.get_available_moves():
            temp_board = deepcopy(board)
            temp_board.make_move(move[0], move[1])
            score = minimax_bruteforce(temp_board, depth + 1, True)
            best_score = min(score, best_score)
        return best_score


def find_best_move_bruteforce(board: Board) -> Tuple[int, int]:
    """Punto de entrada para la IA de fuerza bruta."""
    best_score = -math.inf
    best_move = board.get_available_moves()[0]
    for move in board.get_available_moves():
        temp_board = deepcopy(board)
        temp_board.make_move(move[0], move[1])
        score = minimax_bruteforce(temp_board, 0, False)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


def minimax_alpha_beta(
    board: Board, depth: int, alpha: float, beta: float, is_maximizing: bool
) -> int:
    """Versión optimizada con Poda Alfa-Beta."""
    if board.winner == AI_PLAYER:
        return 1
    if board.winner == HUMAN_PLAYER:
        return -1
    if board.is_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in board.get_available_moves():
            temp_board = deepcopy(board)
            temp_board.make_move(move[0], move[1])
            score = minimax_alpha_beta(temp_board, depth + 1, alpha, beta, False)
            best_score = max(score, best_score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = math.inf
        for move in board.get_available_moves():
            temp_board = deepcopy(board)
            temp_board.make_move(move[0], move[1])
            score = minimax_alpha_beta(temp_board, depth + 1, alpha, beta, True)
            best_score = min(score, best_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score


def find_best_move_alpha_beta(board: Board) -> Tuple[int, int]:
    """Punto de entrada para la IA optimizada."""
    best_score = -math.inf
    best_move = board.get_available_moves()[0]
    for move in board.get_available_moves():
        temp_board = deepcopy(board)
        temp_board.make_move(move[0], move[1])
        score = minimax_alpha_beta(temp_board, 0, -math.inf, math.inf, False)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move
