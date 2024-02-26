from model.game import Game
from view.console_game_view import ConsoleGameView

class GameController:
    def __init__(self, model: Game, view: ConsoleGameView) -> None:
        self.model = model
        self.view = view

    def start_game(self):
        """
        Runs the main loop of the game
        """

        ai_dec = input("would you like to play against AI? (y/n)") == "y"
        if ai_dec:
            depth = int(input("Please enter the difficulty level you would like (1-10)"))
        while not self.model.game_over():
            self.view.display_board()
            self.view.display_current_player()
            self.view.display_score(self.model.get_current_player())
            self.view.display_legal_moves()

            if self.model.current_player == self.model.player1 or self.model.current_player == self.model.player2 and not ai_dec:
                move = self.view.get_move()
                if move == "p":
                    self.model.swap_turns()
                else:
                    row, col = move
                    self.execute_move(row, col)
            elif ai_dec:
                move = self.model.get_best_move(depth)
                self.execute_move(move[0], move[1])

        self.view.display_board()
        winner = self.model.declare_winner()
        if not winner:
            self.view.display_draw_message()
        else:
            self.view.display_winner(winner)

        self.view.display_final_scorebaord()

    # Calls the model to make a move if it is legal
    def execute_move(self, row, col) -> None:
        current_player = self.model.get_current_player()
        if not self.model.is_move_legal(row, col, current_player):
            self.view.display_illegal_move_message()
        else:
            self.model.make_move(row, col)
