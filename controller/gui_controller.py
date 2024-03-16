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