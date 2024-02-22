from model.game import Game
from view.test_board_view import BoardView

class GameController:
    def __init__(self, model: Game, view: BoardView) -> None:
        self.model = model
        self.view = view

    def start_game(self):
        """
        Runs the main loop of the game
        """
        if not self.model.game_over():
            self.view.root.mainloop()

        temp = self.model.declare_winner()
        if temp == None:
            self.view.display_draw_message()
        else:
            self.view.display_winner(temp)

    # Calls the model to make a move if it is legal
    def execute_move(self, row, col) -> None:
        current_player = self.model.get_current_player()
        if not self.model.is_move_legal(row, col, current_player):
            self.view.display_illegal_move_message()
        else:
            self.model.make_move(row, col)
