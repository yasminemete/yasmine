import math
from typing import List
import interfaces
from interfaces import Board


def get_playable_columns(board: interfaces.Board) -> List[int]:
    return [col for col in range(board.width) if board.column(col).count(interfaces.Token.EMPTY) > 0]


def evaluate_position(board: interfaces.Board, player_token: interfaces.Token) -> float:
    return 0


def is_board_full(board: interfaces.Board) -> bool:
    for col in range(board.width):
        if board.column(col).count(interfaces.Token.EMPTY) > 0:
            return False
    return True


def next_open_row(board, col):
    for row in range(board.height - 1, -1, -1):
        if board.box(row, col) == interfaces.Token.EMPTY:
            return row
    return -1


def copy_board(board):
    copied_board: Board = interfaces.Board(board.height, board.width, board.to_win)
    for i in range(board.height):
        for j in range(board.width):
            copied_board.__board[i][j] = board.__board[i][j]
    return copied_board


class yasminedoriaStrategy(interfaces.Strategy):

    @property
    def authors(self) -> str:
        return "Mete-Berend"

    def play(self, current_board: interfaces.Board, your_token: interfaces.Token) -> None:
        depth = 4
        _, column = self.minimax(current_board, depth, your_token, -math.inf, math.inf, True)
        return column

    def minimax(self, board: interfaces.Board, depth: int, player_token: str, alpha: float, beta: float,
                maximizing_player: bool) -> tuple[float, None]:
        if depth == 0 or all(board.column(col).count(interfaces.Token.EMPTY) == 0 for col in range(board.width)):
            return evaluate_position(board, player_token), None

        if maximizing_player:
            max_eval = -math.inf
            best_column = None
            for col in get_playable_columns(board):
                row = next_open_row(board, col)
                temp_board = board.copy()
                temp_board.play(col, player_token)  # Utiliser la méthode play au lieu de drop_token
                eval_val, _ = self.minimax(temp_board, depth - 1, player_token, alpha, beta, False)
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
                row = next_open_row(board, col)
                temp_board = copy_board(board)
                temp_board.play(col, player_token.opponent())  # Utiliser le joueur adverse
                eval_val, _ = self.minimax(temp_board, depth - 1, player_token, alpha, beta, True)
                if eval_val < min_eval:
                    min_eval = eval_val
                    best_column = col
                beta = min(beta, eval_val)
                if beta <= alpha:
                    break
            return min_eval, best_column


def play_connect_four():
    height = 6
    width = 7
    to_win = 4
    current_board = interfaces.Board(height, width, to_win)
    player1_token = interfaces.Token.RED
    player2_token = interfaces.Token.YELLOW
    current_player = player1_token

    strategies = [yasminedoriaStrategy(), None]  # Remplacez par vos propres stratégies

    while True:
        print(current_board)

        strategy = strategies[int(current_player == player2_token)]
        if strategy:  # Si c'est l'IA qui joue
            column = strategy.play(current_board, current_player)
            current_board.play(column, current_player)
        else:  # Si c'est le joueur humain qui joue
            while True:
                try:
                    column = int(input(f"Player {current_player}, choose a column (1-{width}): "))
                    current_board.play(column, current_player)
                    break
                except (ValueError, interfaces.IllegalMove):
                    print("Invalid input or column is full. Try again.")

        if not any(current_board.box(row, col) == current_player for row in range(height) for col in range(width)
                   for dr, dc in ((0, 1), (1, 0), (1, 1), (-1, 1))
                   if 0 <= row + dr * (to_win - 1) < height and 0 <= col + dc * (to_win - 1) < width and all(
            current_board.box(row + k * dr, col + k * dc) == current_player for k in range(to_win))):
            current_player = player2_token if current_player == player1_token else player1_token
            continue

        print(current_board)
        print(f"Player {current_player} wins!")
        break


# Exécution du jeu Puissance 4
if __name__ == "__main__":
    play_connect_four()
