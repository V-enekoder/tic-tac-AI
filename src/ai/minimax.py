# src/ai/minimax.py

import math
from copy import deepcopy
from typing import Dict, List, Tuple

from src.game_logic.board import Board


def minimax_bruteforce(
    board: Board,
    depth: int,
    is_maximizing: bool,
    counter: Dict[str, int],
    maximizing_player_id: int,
) -> int:
    """
    maximizing_player_id: El ID del jugador (IA) que quiere obtener +1.
    """
    counter["nodes"] += 1

    if board.winner is not None and board.winner != 0:
        if board.winner == maximizing_player_id:
            return 1
        else:
            return -1

    if board.is_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in board.get_available_moves():
            temp_board = deepcopy(board)
            temp_board.make_move(move[0], move[1])
            score = minimax_bruteforce(
                temp_board, depth + 1, False, counter, maximizing_player_id
            )
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in board.get_available_moves():
            temp_board = deepcopy(board)
            temp_board.make_move(move[0], move[1])
            score = minimax_bruteforce(
                temp_board, depth + 1, True, counter, maximizing_player_id
            )
            best_score = min(score, best_score)
        return best_score


def minimax_alpha_beta(
    board: Board,
    depth: int,
    alpha: float,
    beta: float,
    is_maximizing: bool,
    counter: Dict[str, int],
    maximizing_player_id: int,  # <--- Nuevo argumento
) -> int:
    counter["nodes"] += 1

    if board.winner is not None and board.winner != 0:
        if board.winner == maximizing_player_id:
            return 1
        else:
            return -1

    if board.is_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in board.get_available_moves():
            temp_board = deepcopy(board)
            temp_board.make_move(move[0], move[1])
            score = minimax_alpha_beta(
                temp_board, depth + 1, alpha, beta, False, counter, maximizing_player_id
            )
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
            score = minimax_alpha_beta(
                temp_board, depth + 1, alpha, beta, True, counter, maximizing_player_id
            )
            best_score = min(score, best_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score


def find_best_move_bruteforce(board: Board) -> Tuple[Tuple[int, int], List[dict]]:
    best_score = -math.inf
    best_move = None
    graph_data = []

    ai_player_id = board.turn
    available_moves = board.get_available_moves()

    if not available_moves:
        return (0, 0), []

    best_move = available_moves[0]

    for move in available_moves:
        temp_board = deepcopy(board)
        temp_board.make_move(move[0], move[1])

        score = minimax_bruteforce(temp_board, 0, False, {"nodes": 0}, ai_player_id)

        graph_data.append(
            {"move": move, "score": score, "board": temp_board.board.tolist()}
        )
        if score > best_score:
            best_score, best_move = score, move

    return best_move, graph_data


def find_best_move_alpha_beta(board: Board) -> Tuple[Tuple[int, int], List[dict]]:
    best_score = -math.inf
    best_move = None
    graph_data = []

    ai_player_id = board.turn
    available_moves = board.get_available_moves()

    if not available_moves:
        return (0, 0), []

    best_move = available_moves[0]

    for move in available_moves:
        temp_board = deepcopy(board)
        temp_board.make_move(move[0], move[1])

        score = minimax_alpha_beta(
            temp_board, 0, -math.inf, math.inf, False, {"nodes": 0}, ai_player_id
        )

        graph_data.append(
            {"move": move, "score": score, "board": temp_board.board.tolist()}
        )
        if score > best_score:
            best_score, best_move = score, move

    return best_move, graph_data


def get_simulation_move_bruteforce(board: Board) -> Tuple[Tuple[int, int], int]:
    """Retorna (mejor_movimiento, total_nodos_evaluados) para la simulación."""

    ai_player_id = board.turn

    moves = board.get_available_moves()
    if not moves:
        return (0, 0), 0

    best_score = -math.inf
    best_move = moves[0]
    total_nodes = 0

    for move in moves:
        temp_board = deepcopy(board)
        temp_board.make_move(move[0], move[1])
        counter = {"nodes": 0}

        score = minimax_bruteforce(temp_board, 0, False, counter, ai_player_id)

        total_nodes += counter["nodes"]
        if score > best_score:
            best_score = score
            best_move = move

    return best_move, total_nodes


def get_simulation_move_alpha_beta(board: Board) -> Tuple[Tuple[int, int], int]:
    """
    Realiza una búsqueda unificada con poda Alfa-Beta.
    Retorna (mejor_movimiento, total_nodos_evaluados).
    """

    ai_player_id = board.turn

    moves = board.get_available_moves()
    if not moves:
        return (0, 0), 0

    best_score = -math.inf
    best_move = moves[0]
    counter = {"nodes": 0}
    alpha, beta = -math.inf, math.inf

    for move in moves:
        temp_board = deepcopy(board)
        temp_board.make_move(move[0], move[1])

        score = minimax_alpha_beta(
            temp_board, 0, alpha, beta, False, counter, ai_player_id
        )

        if score > best_score:
            best_score = score
            best_move = move

        alpha = max(alpha, best_score)

    return best_move, counter["nodes"]
