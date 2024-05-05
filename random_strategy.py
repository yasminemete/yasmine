import secrets

import interfaces


class RandomStrategy(interfaces.Strategy):
    """
    Strategy that plays a valid random move for each play.
    """
    def authors(self) -> str:
        return "Sébastien Vaucher"

    def play(self, current_board: interfaces.Board, your_token: interfaces.Token) -> int:
        playable_columns = [index for index in range(current_board.width) if
                            interfaces.Token.EMPTY in current_board.column(index)]
        return secrets.choice(playable_columns)
