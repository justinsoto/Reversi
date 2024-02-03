class GameController:
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view
    
    def start_game(self):
        """
        Runs the main loop of the game
        """
        #display board
        self.view.display_board()
        while True:
            row, col = self.view.get_move()

            while not self.model.is_legal_move(row, col):
                self.view.show_illegal_move()
                row, col = self.view.get_move()
            
            self.model.make_move(row,col)
            self.view.display_board()

            # Check if game is won 
            winner = self.model.is_game_over()
            if winner != False:
                if winner == None:
                    self.view.show_draw()
                else:
                    self.view.show_winner(winner)
                break

            self.model.switch_players()
