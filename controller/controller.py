from model.game import Game
from model.ai import AI
from view.console_items.console_game_view import ConsoleGameView
from model.ai_strategy import MinimaxStrategy, RandomStrategy, MiniMaxAlphaBeta


class GameController:
    def __init__(self, model: Game, view: ConsoleGameView) -> None:
        self.model = model
        self.view = view
        self.ai_dec = input("would you like to play against AI? (y/n)") == "y"
        if self.ai_dec:
            p = int(input("Would you like to play against random moves (0) or minimax (1)? "))
            if p == 0:
                self.ai = AI(self.model, RandomStrategy(0, self.model))
            elif p == 1:
                depth = int(input("Please enter the difficulty level you would like (1-5) "))
                t = int(input('Would you like to play against minimax (0) or minimax with Alpha Beta Pruning (1)? '))
                if t == 0:
                    self.ai = AI(self.model, MinimaxStrategy(depth, self.model))
                elif t == 1:
                    self.ai = AI(self.model, MiniMaxAlphaBeta(depth, self.model))

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
                move = self.ai.choose_move()
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
        self.view.display_final_scorebaord()

    # Calls the model to make a move if it is legal
    def execute_move(self, row, col) -> None:
        current_player = self.model.get_current_player()
        if not self.model.is_move_legal(row, col, current_player):
            self.view.display_illegal_move_message()
        else:
            self.model.make_move(row, col)
