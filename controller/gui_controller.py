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
        """
        Initializes the GUIController with a game model. This controller adapts game logic to be used with a GUI, 
        typically handling requests and responses instead of direct input/output.

        Parameters:
        model (Game): The game model handling the game logic and state.
        """        
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
        """
        Determines if the AI is in the process of making a move.

        Returns:
        bool: True if AI is enabled and it is currently the AI's turn, False otherwise.
        """        
        return self.aiEnabled and self.model.get_current_player() == self.model.player2

    def execute_move(self, row: int, col: int):
        """
        Executes a move at a specified row and column on the game board.

        Parameters:
        row (int): The row index where the move is to be made.
        col (int): The column index where the move is to be made.
        """        
        self.model.make_move(row, col)

    def get_AI_move(self) -> tuple[int]:
        # If the AI is enabled it will execute a move for player        
        """
        Retrieves the next move from the AI, if AI is enabled and it is the AI's turn.

        Returns:
        tuple[int, int]: The row and column indices of the AI's next move, or (-1, -1) if AI move is not applicable.
        """        
        if self.aiEnabled and self.model.get_current_player() == self.model.player2:
            row, col = self.ai.choose_move()
            return row, col

        return -1, -1

    # Passes turn
    def pass_turn(self):
        """
        Passes the turn to the next player in the game.
        """        
        self.model.swap_turns()

    # Returns the state of the cell, if it's occupied, empty, or a legal space
    def get_cell(self, row, col):
        """
        Retrieves the state of a cell at a specified location.

        Parameters:
        row (int): The row index of the cell.
        col (int): The column index of the cell.

        Returns:
        str: A string indicating if the cell is 'Legal', 'Empty', or contains a player's marker.
        """        
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
        """
        Resets the game to its initial state.
        """        
        self.model.reset_game()

    # Toggles AI status
    # Side Effect: resets the entire game
    def toggle_ai_status(self):
        """
        Toggles the AI's enabled status and resets the game.

        Side Effect:
        Resets the entire game to its initial state.
        """        
        self.aiEnabled = not self.aiEnabled
        self.reset_game()

    # Returns the winner of the game, None if draw
    def get_winner(self):
        """
        Determines the winner of the game.

        Returns:
        The winner of the game or None if the game ends in a draw.
        """        
        return self.model.declare_winner()

    def get_loser(self):
        """
        Determines the loser of the game.

        Returns:
        The loser of the game or None if the game ends in a draw.
        """        
        return self.model.declare_loser()

    # Returns string representation of the player
    def player_to_str(self, player):
        """
        Converts a player identifier to a string representation.

        Parameters:
        player: The player identifier.

        Returns:
        str: A string representing the player.
        """        
        return self.player_to_string[player]