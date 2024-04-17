# this implementation of the controller is for the GUI/React App, transforming the CLI interaction model into
# one that works through http requests and responses. This means this version of the GameController
# would not use input() or print statements.
from time import sleep
from model.game import Game
from model.ai import AI
from model.ai_strategy import MinimaxStrategy, RandomStrategy, MiniMaxAlphaBeta
from firebaseDB.db_facade import database
from time import sleep

class GUIController:
    def __init__(self, model: Game):
        self.model = model
        self.aiEnabled = False
        self.ai = AI(self.model, MiniMaxAlphaBeta(3, self.model))
        self.players = self.model.get_all_players()
        self.player_to_string = {
            self.players[0]: "Player 1",
            self.players[1]: "Player 2"
        }

    # Returns True if the AI is currently in the processing of choosing the next move
    def is_AI_making_move(self) -> bool:
        return self.aiEnabled and self.model.get_current_player() == self.model.player2

    def execute_move(self, row: int, col: int):
        self.model.make_move(row, col)

    def get_AI_move(self) -> tuple[int]:
        # If the AI is enabled it will execute a move for player
        if self.aiEnabled and self.model.get_current_player() == self.model.player2:
            row, col = self.ai.choose_move()
            return row, col

        return -1, -1

    # Passes turn
    def pass_turn(self):
        self.model.swap_turns()

    # Returns the state of the cell, if it's occupied, empty, or a legal space
    def get_cell(self, row, col):
        row, col = int(row), int(col)

        legal_moves = self.model.find_legal_moves()
        if [row, col] in legal_moves:
            return "Legal"

        if not self.model.is_cell_empty(row, col):
            player = self.model.get_player_at_cell(row, col)
            return self.player_to_str(player)

        return "Empty"

    # Sets the game to its initial state
    def reset_game(self):
        self.model.reset_game()

    # Toggles AI status
    # Side Effect: resets the entire game
    def toggle_ai_status(self):
        self.aiEnabled = not self.aiEnabled
        self.reset_game()

    # Returns the winner of the game, None if draw
    def get_winner(self):
        return self.model.declare_winner()

    # Returns string representation of the player
    def player_to_str(self, player):
        return self.player_to_string[player]
