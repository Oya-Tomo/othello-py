from enum import Enum
from copy import deepcopy
import itertools

import pprint

# x, y
FLIP_DIRECTIONS = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


def move_to_pos(move: str) -> tuple:
    return "abcdefgh".find(move[0]), int(move[1]) - 1


def move_to_board(x: int, y: int) -> list:
    board = [[0 for x in range(8)] for y in range(8)]
    board[y][x] = 1
    return board


def out_of_board(x, y) -> bool:
    return not (0 <= x <= 7 and 0 <= y <= 7)


class OthelloPiece(Enum):
    Black = "black"
    White = "white"


class Othello:
    def __init__(self, color: OthelloPiece):
        self.color = color
        self.current_board = None  # initial_board() required.
        self.pool_play_board = []
        self.pool_move_board = []

        self.self_num = (1, 0)
        self.opnt_num = (0, 1)
        self.empty_num = (0, 0)

    def initial_board(self):
        self.current_board = [[self.empty_num for x in range(8)] for y in range(8)]
        if self.color == OthelloPiece.Black:
            self.current_board[3][4] = self.self_num
            self.current_board[4][3] = self.self_num
            self.current_board[3][3] = self.opnt_num
            self.current_board[4][4] = self.opnt_num
        else:
            self.current_board[3][4] = self.opnt_num
            self.current_board[4][3] = self.opnt_num
            self.current_board[3][3] = self.self_num
            self.current_board[4][4] = self.self_num

    def put(self, x, y, color: OthelloPiece, flip_dirs: list):
        if self.color == color:
            self._pool_current_board(x, y)
            self.current_board[y][x] = self.self_num
            for dir in flip_dirs:
                x_dir, y_dir = dir
                for i in range(1, 8):
                    match self.current_board[y + i * y_dir][x + i * x_dir]:
                        case self.self_num:
                            break
                        case self.opnt_num:
                            self.current_board[y + i * y_dir][
                                x + i * x_dir
                            ] = self.self_num
        else:
            self.current_board[y][x] = self.opnt_num
            for dir in flip_dirs:
                x_dir, y_dir = dir
                for i in range(1, 8):
                    match self.current_board[y + i * y_dir][x + i * x_dir]:
                        case self.opnt_num:
                            break
                        case self.self_num:
                            self.current_board[y + i * y_dir][
                                x + i * x_dir
                            ] = self.opnt_num

    def can_put(
        self, x: int, y: int
    ) -> list:  # return directions that you can flip stones.
        if self.current_board[y][x] != self.empty_num:
            return []

        can_flip_dir = []

        for dir in FLIP_DIRECTIONS:
            x_dir, y_dir = dir
            exisis_optn_num = False
            for i in range(1, 8):
                if out_of_board(x + i * x_dir, y + i * y_dir):
                    break
                match self.current_board[y + i * y_dir][x + i * x_dir]:
                    case self.empty_num:
                        break
                    case self.self_num:
                        if exisis_optn_num:
                            can_flip_dir.append(dir)
                            break
                        else:
                            break
                    case self.opnt_num:
                        exisis_optn_num = True

        return can_flip_dir

    def search_putable_pos(self) -> list:
        putable_pos = []
        for y in range(0, 8):
            for x in range(0, 8):
                if len(self.can_put(x, y)) > 0:
                    putable_pos.append((x, y))
        return putable_pos

    def judge_winner(self) -> OthelloPiece:
        board_pieces = list(itertools.chain.from_iterable(self.current_board))
        self_count = board_pieces.count(self.self_num)
        opnt_count = board_pieces.count(self.opnt_num)
        if self_count == opnt_count:
            return None
        elif self_count > opnt_count:
            return self.color
        else:
            return (
                OthelloPiece.White
                if self.color == OthelloPiece.Black
                else OthelloPiece.Black
            )

    def _pool_current_board(self, x: int, y: int):
        self.pool_play_board.append(deepcopy(self.current_board))
        self.pool_move_board.append(move_to_board(x, y))


if __name__ == "__main__":
    SELF_NUM = 2
    OPNT_NUM = 1
    EMPTY_NUM = 0
    black_player = Othello(SELF_NUM, OPNT_NUM, EMPTY_NUM, OthelloPiece.Black)
    black_player.initial_board()

    white_player = Othello(SELF_NUM, OPNT_NUM, EMPTY_NUM, OthelloPiece.White)
    white_player.initial_board()

    move1 = black_player.can_put(4, 5)
    black_player.put(4, 5, OthelloPiece.Black, move1)
    white_player.put(4, 5, OthelloPiece.Black, move1)

    move2 = white_player.can_put(5, 5)
    black_player.put(5, 5, OthelloPiece.White, move2)
    white_player.put(5, 5, OthelloPiece.White, move2)

    move3 = black_player.can_put(5, 4)
    black_player.put(5, 4, OthelloPiece.Black, move3)
    white_player.put(5, 4, OthelloPiece.Black, move3)

    print("black play boards")
    pprint.pprint(black_player.pool_play_board)

    print("black play boards")
    pprint.pprint(black_player.pool_move_board)

    print("white play boards")
    pprint.pprint(white_player.pool_play_board)

    print("white play boards")
    pprint.pprint(white_player.pool_move_board)
