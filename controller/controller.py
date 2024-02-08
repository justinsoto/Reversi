from model.game import Game
from view.console_board_view import ConsoleBoardView

class GameController:
    def __init__(self, model: Game, view: ConsoleBoardView) -> None:
        self.model = model
        self.view = view
    
    def start_game(self):
        """
        Runs the main loop of the game
        """
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
                self.execute_move(row, col)

        self.view.display_board()
        winner = self.model.declare_winner()
        if not winner:
            self.view.display_draw_message()
        else:
            self.view.display_winner(winner)
        
        self.view.display_final_scorebaord()

    def get_move(self) -> [int, int]:
        move = input('Enter your move (row, col): ')

        # Pass turn key
        if move == "p":
            return move
        
        values = move.split(',')
        row, col = int(values[0]), int(values[1])
        return row, col
    
    # Calls the model to make a move if it is legal
    def execute_move(self, row, col) -> None:
        current_player = self.model.get_current_player()
        if not self.model.is_move_legal(row, col, current_player):
            self.view.display_illegal_move_message()
        else:
            self.model.make_move(row, col)

