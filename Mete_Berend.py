import copy
import math
from typing import List
import interfaces
from interfaces import *


def get_playable_columns(board: interfaces.Board) -> List[int]:
    """
    Permet de retourner une liste des colonnes jouables
    """
    return [col for col in range(board.width) if board.column(col).count(interfaces.Token.EMPTY) > 0]


def evaluate_position(board: interfaces.Board, player_token: interfaces.Token) -> float:
    """
    Évalue la position actuelle du jeu
    """
    score = 0
    opponent = opponent_token(player_token)

    # Check pour un coup gagnant pour le joueur
    for col in range(board.width):
        temp_board = copy.deepcopy(board)
        if temp_board.column(col).count(interfaces.Token.EMPTY) > 0:
            temp_board.play(col, player_token)
            if winning_line(temp_board):
                score += 100

    # Check pour un coup gagnant pour l'adversaire
    for col in range(board.width):
        temp_board = copy.deepcopy(board)
        if temp_board.column(col).count(interfaces.Token.EMPTY) > 0:
            temp_board.play(col, opponent)
            if winning_line(temp_board):
                score -= 100

    return score


def opponent_token(your_token: interfaces.Token) -> interfaces.Token:
    """
    Retourne le jeton de l'adversaire
    """
    return interfaces.Token.RED if your_token == interfaces.Token.YELLOW else interfaces.Token.YELLOW


def winning_line(board: interfaces.Board) -> bool:
    """
    Vérifie s'il y a un alignement possible de 4 jetons.
    """
    # Vérifie les lignes horizontales
    for row in range(board.height):
        for col in range(board.width - 3):
            if all(board.box(row, col + i) != interfaces.Token.EMPTY for i in range(4)):
                if len(set(board.box(row, col + i) for i in range(4))) == 1:
                    return True
    # Vérifie les colonnes verticales
    for col in range(board.width):
        for row in range(board.height - 3):
            if all(board.box(row + i, col) != interfaces.Token.EMPTY for i in range(4)):
                if len(set(board.box(row + i, col) for i in range(4))) == 1:
                    return True
    # Vérifie les diagonales
    for row in range(board.height - 3):
        for col in range(board.width - 3):
            if all(board.box(row + i, col + i) != interfaces.Token.EMPTY for i in range(4)):
                if len(set(board.box(row + i, col + i) for i in range(4))) == 1:
                    return True
    # Vérifie les autres diagonales
    for row in range(board.height - 3):
        for col in range(3, board.width):
            if all(board.box(row + i, col - i) != interfaces.Token.EMPTY for i in range(4)):
                if len(set(board.box(row + i, col - i) for i in range(4))) == 1:
                    return True
    return False


class yasmine_doriaStrategy(interfaces.Strategy):
    """
    Strategie qui joue un coup gagnant possible ou bloque un coup gagnant adverse, si possible
    """
    depth = 4

    def authors(self) -> str:
        return "Mete-Berend"

    def play(self, current_board: interfaces.Board, your_token: interfaces.Token) -> None:
        """
        Retourne la colonne à jouer en appelant l'algorithme minimax
        """
        _, column = self.minimax(current_board, your_token, depth=yasmine_doriaStrategy.depth, alpha=-math.inf,
                                 beta=math.inf, maximizing_player=True)

        return column

    def minimax(self, board: Board, token: Token, depth: int, alpha: float, beta: float,
                maximizing_player: bool) -> int:
        """
        Implémentation de l'algorithme minimax avec élagage alpha-beta
        """
        if depth == 0 or all(board.column(col).count(interfaces.Token.EMPTY) == 0 for col in range(board.width)):
            return evaluate_position(board, token), None

        if maximizing_player:
            max_eval = -math.inf
            best_column = None
            for col in get_playable_columns(board):
                temp_board = copy.deepcopy(board)
                temp_board.play(col, token)  # Utiliser la méthode play au lieu de drop_token
                eval_val, _ = self.minimax(temp_board, token, depth - 1, alpha, beta, False)
                if eval_val > max_eval:
                    max_eval = eval_val
                    best_column = col
                alpha = max(alpha, eval_val)
                if beta <= alpha:
                    break
            return max_eval, best_column
        else:
            min_eval = math.inf
            best_column = None
            for col in get_playable_columns(board):
                temp_board = copy.deepcopy(board)
                temp_board.play(col, opponent_token(token))  # Utiliser le joueur adverse
                eval_val, _ = self.minimax(temp_board, token, depth - 1, alpha, beta, True)
                if eval_val < min_eval:
                    min_eval = eval_val
                    best_column = col
                beta = min(beta, eval_val)
                if beta <= alpha:
                    break
            return min_eval, best_column
