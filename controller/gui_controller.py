# this implementation of the controller is for the GUI/React App, transforming the CLI interaction model into
# one that works through http requests and responses. This means this version of the GameController
# would not use input() or print statements.
from model.game import Game

class GUIController:
    def __init__(self, model: Game):
        self.model = model

    def execute_move(self, row: int, col: int):
        self.model.make_move(row, col)

    def pass_turn(self):
        self.model.swap_turns()

    def get_cell(self, row, col):
        row, col = int(row), int(col)

        players = self.model.get_all_players()
        player_to_string = {
            players[0]: "Player 1",
            players[1]: "Player 2"
        }

        legal_moves = self.model.find_legal_moves()
        if [row, col] in legal_moves:
            return "Legal"
        
        if not self.model.is_cell_empty(row, col):
            player = self.model.get_player_at_cell(row, col)
            return player_to_string[player]
        
        return "Empty"
    
    def reset_game(self):
        self.model.reset_game()