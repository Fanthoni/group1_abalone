import enum
import sys

from abalone import Abalone
from board import Board, BoardTile
from heuristic import Heuristic


class InfiniteValues(enum.IntEnum):
    NEG_INF = sys.maxsize * -1
    POS_INF = sys.maxsize


class Search:
    def __init__(self, state):
        self.state = state  # State is a board object
        self.starting_depth = 3
        self.alpha = InfiniteValues.NEG_INF
        self.beta = InfiniteValues.POS_INF
        self.dict = {}

    def terminal_test(self):
        return False

    def ab_search(self):
        depth = 3
        value = self.max_value(self.state, depth)
        print("Overall:", value)
        print(self.dict)
        return value

    def max_value(self, state, depth):
        if self.terminal_test() or depth == 0:
            return Heuristic.evaluate_board(state)

        value = InfiniteValues.NEG_INF

        groups = state.get_marble_groups(BoardTile.BLUE)
        valid_moves = state.generate_moves(groups)

        for action in valid_moves:  # Generate list of all possible moves from current state
            new_state = state.get_board_after_move(action)
            value = max(value, self.min_value(new_state, depth - 1))

            if value > self.beta:
                return value
            self.alpha = max(self.alpha, value)
        return value

    def min_value(self, state, depth):
        if self.terminal_test() or depth == 0:
            return Heuristic.evaluate_board(state)

        value = InfiniteValues.POS_INF

        groups = state.get_marble_groups(BoardTile.RED)
        valid_moves = state.generate_moves(groups)

        for action in valid_moves:  # Generate list of all possible moves from current state
            new_state = state.get_board_after_move(action)
            value = min(value, self.max_value(new_state, depth - 1))

            if value < self.alpha:
                return value
            self.beta = min(self.beta, value)
        return value


def main():
    abalone = Abalone()
    abalone.setup_from_input_file("Test1.input")
    board = abalone.board

    ab_search = Search(board)
    val = ab_search.ab_search()
    board.print_board()




if __name__ == "__main__":
    main()