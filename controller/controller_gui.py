# this implementation of the controller is for the GUI/React App, transforming the CLI interaction model into
# one that works through http requests and responses. This means this version of the GameController
# would not use input() or print statements.
from model.game import Game
from model.ai import ai

class GameControllerGUI:
    def __init__(self, model: Game, ai_decision: bool, ai_depth: int = 3) -> None:
        self.model = model
        self.ai_dec = ai_decision
        if self.ai_dec:
            self.ai = ai(self.model, ai_depth)

    def start_game(self):
        # initialize or reset the game as needed
        pass # TODO: Implement this function later

    def make_move(self, row: int, col: int):
        # handle making a move in the game, possibly returning the updated game state
        pass # TODO: Implement this function later

    def get_game_state(self):
        # return the current state of the game, suitable for sending to the frontend
        pass # TODO: Implement this function later
