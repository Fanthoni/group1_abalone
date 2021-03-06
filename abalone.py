from board import StartingPositions, Board, BoardTile
from player import HumanPlayer, AIPlayer
from move import Move
from ab_search_optimize import Search
import random


class Abalone:
    """
    WIP - ac
    """

    def __init__(self):
        self.players = {"Black": None, "White": None}
        self._current_player = "Black"
        self._is_game_paused = False
        self._is_game_stopped = False
        self._game_mode = StartingPositions.BELGIAN
        self._board = Board(self._game_mode)

    def start_game(self):
        """
        Starts the game and contains game logic.
        :return:
        """
        self.board = Board(self._game_mode)
        self.board.print_board()

        if self._players["Black"] is None or self._players["White"] is None:
            print("Please ensure both players are set!")

        if type(self._players["Black"]) == AIPlayer and type(self._players["White"]) == AIPlayer:
            print("We do not support two AIs playing against each other yet. Please reconfigure players.")
            return

        first_move = True

        while not self.is_game_stopped:
            # Our Player class will handle their own timers, moves, and previous moves.
            if self._current_player == "Black":
                if type(self._players.get("Black")) == AIPlayer:
                    print("---Black (AI)---")
                    if first_move:
                        groups = self.board.get_marble_groups(BoardTile.BLUE)
                        moves = self.board.generate_moves(groups)
                        random_move = moves[random.randint(0, len(moves)-1)]
                        self.board.update_board(random_move)
                        self.board.print_board()
                        first_move = False
                    else:
                        self.ai_moves()
                else:
                    print("---Black (Player)---")
                    self.player_moves()
                self._current_player = "White"
            elif self._current_player == "White":
                if type(self._players.get("White")) == AIPlayer:
                    print("---White (AI)---")
                    self.ai_moves()
                else:
                    print("---White (Player)---")
                    self.player_moves()
                self._current_player = "Black"

        self.reset_game()

    def ai_moves(self):
        print("Time remaining: X")
        print("Moves remaining: X")
        print("Previous Moves: ...")
        print("Next Move = X")
        print("Time used to decide this move: X")

        print("Black : 0 - 0 : White")  # Scoreboard
        print("AI is thinking of a move!")
        ab_search = Search()
        self.board.update_board(ab_search.ab_search(self._board, self.current_player))

        print("AI Player made a move!")
        self.board.print_board()

    def player_moves(self):
        """
        For UI demonstration purposes only - Player class not implemented yet.
        :return:
        """
        print("Time remaining: X")
        print("Moves remaining: X")
        Abalone.print_menu_options()

        moved = False
        while not moved:
            user_input = input("Input: ")
            match user_input:
                case "1":
                    self.board.update_board(Move.from_string(input("Enter Move Information: ")))
                    print("Time taken for this move: X")
                    moved = True
                    print(f"Black : {self.board.blue_score} - {self.board.red_score} : White")  # Scoreboard
                    self.board.print_board()
                case "2":
                    print("Previous moves: ...")
                case "3":
                    self.undo_last_move()
                case "4":
                    self.pause_game()
                    input("Enter anything to resume: ")
                    self.resume_game()
                case "5":
                    self.stop_game()
                    break

    @staticmethod
    def print_menu_options():
        """
        Prints in-game menu options.
        :return:
        """
        print("1. Make Move\n"
              "2. View Previous Moves\n"
              "3. Undo Move\n"
              "4. Pause Game\n"
              "5. Stop Game")

    def color_selection(self):
        pass

    def set_move_limit(self):
        pass

    def set_time_limit(self):
        pass

    def set_start_positions(self, enum_value):
        """
        Sets the starting positions.
        :param enum_value:
        :return:
        """
        if enum_value in (StartingPositions.DEFAULT, StartingPositions.GERMAN, StartingPositions.BELGIAN):
            self._game_mode = enum_value

    def undo_last_move(self):
        """
        Undo the last move made.
        :return:
        """
        print("Move undone!")

    def pause_game(self):
        """
        Pause the game.

        :return: None
        """
        print("Game paused")
        self.is_game_paused = True

    def resume_game(self):
        """
        Resume game after it's been paused.

        :return: None
        """
        print("Game resumed")
        self.is_game_paused = False

    def reset_game(self):
        """
        Assists in resetting the Abalone object after stopping game.

        :return: None
        """
        self.is_game_paused = False
        self.is_game_stopped = False

    def stop_game(self):
        """
        Stops the game.

        :return: None
        """
        print("Game stopped")
        self.is_game_stopped = True

    @property
    def is_game_paused(self):
        """
        Returns value for if the game is paused or not.

        :return: None
        """
        return self._is_game_paused

    @is_game_paused.setter
    def is_game_paused(self, paused):
        """
        Sets the value for if game is paused or not.
        :param paused: boolean (True/False)

        :return: None
        """
        self._is_game_paused = paused

    @property
    def is_game_stopped(self):
        """
        Returns value for if game is stopped or not.

        :return: None
        """
        return self._is_game_stopped

    @is_game_stopped.setter
    def is_game_stopped(self, stopped):
        """
        Sets value for if game is stopped or not
        :param stopped: boolean (True/False)

        :return: None
        """
        self._is_game_stopped = stopped

    def set_player1(self, player):
        """
        Sets a player to black.
        """
        self.players["Black"] = player

    def set_player2(self, player):
        """
        Sets a player to white.
        """
        self.players["White"] = player

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board):
        self._board = board

    def setup_from_input_file(self, file_name):
        """
        Takes an input file as input, translates it into a board layout and sets a player to the current player.
        :param file_name: input file

        :return: None
        """
        self.board = Board(StartingPositions.EMPTY)
        with open(file_name, 'r') as file:
            data = file.readlines()
            moves = data[1].strip('\n').split(',')

        key = "White" if data[0].strip('\n') == "w" else "Black"
        self._current_player = key

        self.board.setup_board_from_moves(moves)

    @property
    def current_player(self):
        return self._current_player

    @property
    def player1(self):
        return self._players["Black"]

    @property
    def player2(self):
        return self._players["White"]

    def reset_board(self):
        self.board = Board(self._game_mode)


def main():
    abalone = Abalone()
    input_file_name = input("Enter the file name: ")
    abalone.setup_from_input_file(input_file_name)
    abalone.board.generate_all_possible_moves_and_resulting_boards(abalone.current_player, input_file_name)


if __name__ == "__main__":
    main()

