from model.board import Board
from model.player_color import PlayerColor, color_to_symbol
from model.player import Player
from model.game_state import GameState
from model.prototype import Prototype
import json
import copy


class Game(Prototype):
    def __init__(self, size, player1ID, player2ID) -> None:
        """
        Initializes a new game instance with specified players and board size.

        Parameters:
        size (int): The size of the board (n x n).
        player1ID (str): Identifier for the first player, who will play as Black.
        player2ID (str): Identifier for the second player, who will play as White.
        """        
        self.player1 = Player(PlayerColor.Black, player1ID)
        self.player2 = Player(PlayerColor.White, player2ID)
        self.board = Board(size)
        self.size = size
        self.current_player = self.player1
        self.player_scores = {self.player1: 2,
                              self.player2: 2}
        self.move_dirs = [(-1, -1), (-1, 0),
                          (-1, +1), (0, -1),
                          (0, +1), (+1, -1),
                          (+1, 0), (+1, +1)]
        self.state_history = []

    # Returns a deep copy of this Game object
    def clone(self):
        """
        Creates a deep copy of the game instance, allowing for simulations and undo functionality without affecting the original game state.

        Returns:
        Game: A deep copy of this game instance.
        """        
        return copy.deepcopy(self)

    # Returns a copy of the board
    def get_board(self):
        """
        Retrieves a copy of the game board.

        Returns:
        Board: A copy of the current game board state.
        """        
        return self.board.clone()

    # Returns the current player
    def get_current_player(self):
        """
        Gets the player whose turn is currently active.

        Returns:
        Player: The current player.
        """        
        return self.current_player

    # Returns all scores
    def get_scores(self):
        """
        Retrieves the current scores of both players.

        Returns:
        dict: A dictionary containing the scores of each player.
        """        
        return self.player_scores

    # Returns this player's score (number of pieces)
    def get_player_score(self, player: Player) -> int:
        """
        Retrieves the score of a specific player.

        Parameters:
        player (Player): The player whose score is being queried.

        Returns:
        int: The current score of the specified player.
        """        
        return self.player_scores[player]

    # Returns the current player's color
    def get_current_player_color(self):
        """
        Retrieves the color of the current player.

        Returns:
        PlayerColor: The color of the current player.
        """        
        return self.current_player.get_color()

    # Returns the size of the game board
    def get_board_size(self):
        """
        Retrieves the size of the board.

        Returns:
        int: The size of the game board.
        """        
        return self.size

    # Returns all players in the game
    def get_all_players(self):
        """
        Lists all players involved in the game.

        Returns:
        list: A list of all players.
        """        
        return [player for player in self.player_scores.keys()]

    # Returns player at cell, None if empty
    def get_player_at_cell(self, row, col):
        """
        Determines the player occupying a specific cell on the board.

        Parameters:
        row (int): The row index of the cell.
        col (int): The column index of the cell.

        Returns:
        Player/None: The player occupying the cell, or None if the cell is empty.
        """        
        # Gets the color stored in cell
        color = self.board.get_cell(row, col)
        for player in self.get_all_players():
            if player.get_color() == color:
                return player

        # Cell is empty if this point is reached
        return None

    # Returns True if cell is empty
    def is_cell_empty(self, row, col):
        """
        Checks if a specified cell is empty.

        Parameters:
        row (int): The row index of the cell.
        col (int): The column index of the cell.

        Returns:
        bool: True if the cell is empty, False otherwise.
        """        
        return self.board.is_cell_empty(row, col)

    # Executes move on the given cell coordinates if the move is legal
    # Allows reattempt if move is illegal
    def make_move(self, row, col):
        """
        Executes a move on the board if it is legal.

        Parameters:
        row (int): The row index where the move is to be made.
        col (int): The column index where the move is to be made.

        Note:
        This method will also update scores and swap turns if the move is executed.
        """        
        if self.is_move_legal(row, col, self.current_player):
            self.board.fill_cell(row, col, self.get_current_player_color())
            self.flip_pieces(row, col)
            self.update_scores()
            self.swap_turns()

    # Determines if this player a legal move left to play
    def has_legal_move_remaining(self, player: Player):
        """
        Checks if the specified player has any legal moves left.

        Parameters:
        player (Player): The player to check for legal moves.

        Returns:
        bool: True if there are legal moves available, False otherwise.
        """        
        for row in range(self.size):
            for col in range(self.size):
                if self.is_move_legal(row, col, player):
                    return True
        return False

    # Checks if the player's move is legal
    def is_move_legal(self, row, col, player: Player) -> bool:
        """
        Determines if a move is legal for the specified player at the given coordinates.

        Parameters:
        row (int): The row index of the proposed move.
        col (int): The column index of the proposed move.
        player (Player): The player making the move.

        Returns:
        bool: True if the move is legal, False otherwise.
        """        
        return self.is_valid_coord(row, col) \
                and self.is_cell_empty(row, col) \
                and player == self.current_player \
                and True in [self.has_piece_to_flip(row, col, direction) for direction in self.move_dirs]

    # Checks if the player's move can flip a piece in the given direction
    def has_piece_to_flip(self, row, col, direction) -> bool:
        """
        Determines whether a potential move at the specified location can flip one or more of the opponent's pieces in a given direction. The method checks for a sequence of opponent pieces directly in line and adjacent in the specified direction, ending with a piece of the current player's color.

        Parameters:
        row (int): The row index of the starting cell for checking.
        col (int): The column index of the starting cell for checking.
        direction (tuple): A tuple (dx, dy) where 'dx' and 'dy' represent the directional increments along the row and column, respectively.

        Returns:
        bool: True if executing a move at the specified row and column can flip at least one opponent's piece in the given direction; otherwise, False.
        """        

        start_x, start_y = row, col
        x, y = direction

        while self.is_valid_coord(row + x, col + y):
            # Disqualify this direction if the adjacent cell is empty
            if self.is_cell_empty(row + x, col + y):
                break
            # Disqualify this direction if the adjacent piece belongs to the curerent player
            if self.current_player \
                    == self.get_player_at_cell(start_x + x, start_y + y):
                break
            # Return true if the current place has a non-adjacent piece in the given direction
            if self.current_player \
                    == self.get_player_at_cell(row + x, col + y):
                return True
            # Update cell location
            row += x
            col += y

        return False

    # Flips pieces based on current move
    def flip_pieces(self, row, col) -> None:
        """
        Flips opponent's pieces affected by a move at the specified location.

        Parameters:
        row (int): The row index of the move.
        col (int): The column index of the move.
        """        
        curr_tile = self.current_player.get_color()
        start_x, start_y = row, col
        for direction in self.move_dirs:
            x, y = direction
            row, col = start_x, start_y
            if self.has_piece_to_flip(row, col, direction):
                while self.is_valid_coord(row + x, col + y):
                    row += x
                    col += y
                    if self.board.get_cell(row, col) == curr_tile:
                        break
                    else:
                        self.board.fill_cell(row, col, curr_tile)

    # Checks if a move's coordinates are within board coordinates
    def is_valid_coord(self, row, col) -> bool:
        """
        Checks if the specified coordinates are within the bounds of the board.

        Parameters:
        row (int): The row index to check.
        col (int): The column index to check.

        Returns:
        bool: True if the coordinates are within the board, False otherwise.
        """        
        return 0 <= row < self.size and 0 <= col < self.size

    # Gives turn to other player
    def swap_turns(self) -> None:
        """
        Alternates the turn between the two players.
        """        
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    # Prints cell coordinates of all legal moves available to the current player
    def find_legal_moves(self):
        """
        Identifies all legal moves available to the current player.

        Returns:
        list: A list of coordinates (row, col) where the current player can legally place a piece.
        """        
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.is_move_legal(row, col, self.current_player):
                    moves.append([row, col])
        return moves

    # Restores the game's initial state
    def reset_game(self):
        """
        Resets the game to its initial state, reinitializing the board and resetting player scores.
        """        
        self.board.set_up_board()
        self.current_player = self.player1
        self.update_scores()

    # Checks if the game is over, the game is over when no legal moves
    # remain for either player
    def game_over(self) -> bool:
        """
        Determines if the game has ended, which occurs when neither player has any legal moves remaining.

        Returns:
        bool: True if the game is over, False otherwise.
        """        
        return not self.has_legal_move_remaining(self.player1) \
                and not self.has_legal_move_remaining(self.player2)

    # Returns the winning player, None if the game ends in draw
    def declare_winner(self) -> Player:
        """
        Identifies the winning player based on who has the higher score at the end of the game. If the scores are equal, returns None for a draw.

        Returns:
        Player/None: The player with the highest score, or None if the game is a draw.
        """        
        scores = self.player_scores.values()

        # Handles draw
        if len(set(scores)) == 1:
            return None

        winning_score = max(self.player_scores.values())
        for player in self.get_all_players():
            if self.player_scores[player] == winning_score:
                return player

    def declare_loser(self) -> Player:
        """
        Identifies the losing player based on who has the lowest score at the end of the game. If the scores are equal, returns None for a draw.

        Returns:
        Player/None: The player with the lowest score, or None if the game is a draw.
        """        
        scores = self.player_scores.values()

        # Handles draw
        if len(set(scores)) == 1:
            return None

        losing_score = min(self.player_scores.values())
        for player in self.get_all_players():
            if self.player_scores[player] == losing_score:
                return player

    # Stores the current state of the game
    def store_game_state(self):
        """
        Saves the current state of the game for potential retrieval or undo functionality.
        """        
        state = GameState(self.current_player, self.player_scores, self.board)
        self.state_history.append(state)

    # Loads game from saved game state
    def load_game_state(self, state: GameState):
        """
        Loads a game state, updating the current game to reflect the specified state.

        Parameters:
        state (GameState): The game state to load.
        """        
        self.current_player = state.current_player
        self.player_scores = state.scores
        self.board = state.board

    # Updates both players' scores
    def update_scores(self) -> None:
        """
        Updates the scores of both players based on the current board state.
        """        
        self.player_scores[self.player1] = 0
        self.player_scores[self.player2] = 0

        for row in range(self.size):
            for col in range(self.size):
                player = self.get_player_at_cell(row, col)
                if player:
                    self.player_scores[player] += 1

    #serializes game state to pass to store game state in database
    def serialize_game_state(self):
        """
        Serializes the current state of the game for storage or network transmission.

        Returns:
        str: A JSON string representing the current game state.
        """        
        game_state = {
            'current_player_symbol': color_to_symbol[self.get_current_player_color()],
            'board': [[color_to_symbol[cell] for cell in row] for row in self.board.get_board()],
            'player_scores':{color_to_symbol[self.player1.get_color()]: self.get_player_score(self.player1),
                             color_to_symbol[self.player2.get_color()]: self.get_player_score(self.player2)},
        }
        return json.dumps(game_state)

    #deserialize game state to reconstruct game from game state stored in database
    def deserialize_game_state(self, json_string):
        """
        Deserializes a JSON string representing a game state into an actual GameState object and loads it into the game.

        Parameters:
        json_string (str): The JSON string containing the game state information.
        """        
        game_state = json.loads(json_string)
        board_size = len(game_state['board'])
        current_player_symbol = game_state['current_player_symbol']
        board_data = game_state['board']

        for player in self.get_all_players():
            if color_to_symbol[player.get_color()] == current_player_symbol:
                current_player = player

        board = Board(board_size)
        for row in range(board_size):
            for col in range(board_size):
                cell_symbol = board_data[row][col]
                cell_color = None
                for color, symbol in color_to_symbol.items():
                    if symbol == cell_symbol:
                        cell_color = color
                    board.fill_cell(row,col,cell_color)

        player1_score = game_state['player_scores'][color_to_symbol[self.player1.get_color()]]
        player2_score = game_state['player_scores'][color_to_symbol[self.player2.get_color()]]
        player_scores = {
            self.player1: player1_score,
            self.player2: player2_score
        }

        state = GameState(current_player, player_scores, board)
        self.load_game_state(state)