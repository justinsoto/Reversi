from model.game import Game
from model.ai import ai
from view.console_game_view import ConsoleGameView
from mysql.connector import connect, Error
from getpass import getpass
from model.db_management.user_manager import UserManager
from model.db_management.games_manager import GamesManager
from model.db_management.ratings_manager import RatingsManager
from model.db_management.leaderboard_manager import LeaderboardManager


class GameController:
    def __init__(self, model: Game, view: ConsoleGameView) -> None:
        self.model = model
        self.view = view
        self.ai_dec = input("would you like to play against AI? (y/n)") == "y"
        if self.ai_dec:
            depth = int(input("Please enter the difficulty level you would like (1-5)"))
            while depth < 1 or depth > 5:
                print("Invalid Selection")
                depth = int(input("Please enter the difficulty level you would like (1-5)"))
            self.ai = ai(self.model, depth)

    def start_game(self):
        """
        Runs the main loop of the game
        """
        while not self.model.game_over():
            self.view.display_board()
            self.view.display_current_player()
            self.view.display_score(self.model.get_current_player())
            self.view.display_legal_moves()

            if self.model.current_player == self.model.player1 or self.model.current_player == self.model.player2 and not self.ai_dec:
                move = self.view.get_move()
                if move == "p":
                    self.model.swap_turns()
                else:
                    row, col = move
                    self.execute_move(row, col)
            elif self.ai_dec:
                move = self.ai.get_best_move()
                self.execute_move(move[0], move[1])

        self.view.display_board()
        winner = self.model.declare_winner()
        if not winner:
            self.view.display_draw_message()
        else:
            self.view.display_winner(winner)

        if winner == self.model.player1:
            loser = self.model.player2
        else:
            loser = self.model.player1

        #Viraj - I'm a little confused on what we're going to be adding to the leaderboard so I'm not going to implement it yet

        self.view.display_final_scorebaord()

    # Calls the model to make a move if it is legal
    def execute_move(self, row, col) -> None:
        current_player = self.model.get_current_player()
        if not self.model.is_move_legal(row, col, current_player):
            self.view.display_illegal_move_message()
        else:
            self.model.make_move(row, col)
