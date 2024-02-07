from model.game import Game
from view.board_view import BoardView

class GameController:
    def __init__(self, model: Game, view: BoardView) -> None:
        self.model = model
        self.view = view
    
    def start_game(self):
        """
        Runs the main loop of the game
        """
        #display board
        print(self.view)
        while not self.model.game_over():
            self.view.display_board()
            self.view.display_current_player()
            self.view.display_score(self.model.get_current_player_color())
            self.view.display_legal_moves()
           
            row, col = self.get_move()
            self.model.make_move(row, col)

        self.model.print_winner()

    def get_move(self) -> [int, int]:
        move = input('Enter your move (row, col): ')
        values = move.split(',')
        row, col = int(values[0]), int(values[1])
        return row, col
