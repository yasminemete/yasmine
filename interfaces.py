from abc import abstractmethod, ABC
from enum import Enum


class Token(Enum):
    EMPTY = "ø"
    RED = "R"
    YELLOW = "Y"


class IllegalMove(Exception):
    pass


class Board:
    def __init__(self, height, width, to_win):
        self.height = height
        self.width = width
        self.to_win = to_win
        self.__board = [[Token.EMPTY for _ in range(width)] for _ in range(height)]

    def __repr__(self) -> str:
        return "\n".join(" ".join(token.value for token in line) for line in self.__board)

    def box(self, line_index: int, column_index: int) -> Token:
        return self.__board[line_index][column_index]

    def line(self, index: int) -> list[Token]:
        return self.__board[index]

    def column(self, index: int) -> list[Token]:
        return [line[index] for line in self.__board]

    def diagonals(self):
        for diagonal_index in range(self.width + self.height - 1):
            # south-west to north-east starting at north-western corner
            yield [self.__board[line_index][column_index]
                   for line_index, column_index in
                   zip(range(diagonal_index, -1, -1), range(0, diagonal_index + 1))
                   if line_index < self.height and column_index < self.width
                   ]
            # south-east to north-west starting at north-eastern corner
            yield [self.__board[line_index][column_index]
                   for line_index, column_index in
                   zip(range(diagonal_index, -1, -1), range(self.width - 1, self.width - diagonal_index - 2, -1))
                   if line_index < self.height and column_index >= 0
                   ]

    def play(self, column_index: int, token: Token) -> None:
        column = self.column(column_index)
        try:
            drop_height = self.height - 1 - column[::-1].index(Token.EMPTY)
        except ValueError:
            raise IllegalMove("Column is already full")
        self.__board[drop_height][column_index] = token


class Strategy(ABC):
    @abstractmethod
    def authors(self) -> str:
        """
        The name of the authors who are part of the groups.
        Returns:
            The authors' name.
        """
        pass

    @abstractmethod
    def play(self, current_board: Board, your_token: Token) -> int:
        """
        Hook that needs to compute a move.
        Args:
            current_board: Current state of the game
            your_token: Which tokens your player uses
        Returns:
            The column index to play
        """
        pass
