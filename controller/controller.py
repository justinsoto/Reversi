from model.game import Game

class GameController:
    def __init__(self, model:Game, view) -> None:
        self.model = model
        self.view = view
    
    def start_game(self):
        """
        Runs the main loop of the game
        """
        #display board
        print(self.view)
        while not self.model.game_over():
            #self.view.display_board()
            self.view.show_curr_player()
            self.model.print_score()
            self.model.print_legal_moves()
            row, col = self.view.get_move()
            self.model.make_move(row, col)
            print(self.view)
        self.model.print_winner()
