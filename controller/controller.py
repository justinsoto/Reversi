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
            self.view.display_score(self.model.get_current_player())
            self.view.display_legal_moves()
           
            move = self.get_move()
            if move == "p":
                self.model.swap_turns()
            else:
                row, col = move
                self.model.make_move(row, col)

        self.view.display_board()
        winner = self.model.declare_winner()
        if not winner:
            self.view.display_draw_message()
        else:
            self.view.display_winner(winner)
            self.view.display_score(winner)

    def get_move(self) -> [int, int]:
        move = input('Enter your move (row, col): ')

        # Pass turn key
        if move == "p":
            return move
        
        values = move.split(',')
        row, col = int(values[0]), int(values[1])
        return row, col
