from model.board import Board
from model.player_color import PlayerColor
from model.player import Player
from model.player_color import color_to_symbol
from model.game_state import GameState
from model.prototype import Prototype
import json


class Game(Prototype):
    def __init__(self, size) -> None:
        self.player1 = Player(PlayerColor.Black)
        self.player2 = Player(PlayerColor.White)
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
        clone = Game(self.size)
        state = GameState(self.current_player, self.player_scores, self.get_board())
        clone.load_game_state(state)
        return clone

    # Returns a copy of the board
    def get_board(self):
        return self.board.clone()

    # Returns the current player
    def get_current_player(self):
        return self.current_player

    # Returns all scores
    def get_scores(self):
        return self.player_scores

    # Returns this player's score (number of pieces)
    def get_player_score(self, player: Player) -> int:
        return self.player_scores[player]

    # Returns the current player's color
    def get_current_player_color(self):
        return self.current_player.get_color()

    # Returns the size of the game board
    def get_board_size(self):
        return self.size

    # Returns all players in the game
    def get_players(self):
        return list(self.player_scores.keys())

    # Returns player at cell, None if empty
    def get_player_at_cell(self, row, col):
        # Gets the color stored in cell
        color = self.board.get_cell(row, col)
        for player in self.get_players():
            if player.get_color() == color:
                return player

        # Cell is empty if this point is reached
        return None

    # Returns True if cell is empty
    def is_cell_empty(self, row, col):
        return self.board.is_cell_empty(row, col)

    # Executes move on the given cell coordinates if the move is legal
    # Allows reattempt if move is illegal
    def make_move(self, row, col):
        if self.is_move_legal(row, col, self.current_player):
            self.board.fill_cell(row, col, self.get_current_player_color())
            self.flip_pieces(row, col)
            self.update_scores()
            self.swap_turns()

    # Determines if this player a legal move left to play
    def has_legal_move_remaining(self, player: Player):
        for row in range(self.size):
            for col in range(self.size):
                if self.is_move_legal(row, col, player):
                    return True
        return False

    # Checks if the player's move is legal
    def is_move_legal(self, row, col, player: Player) -> bool:
        return self.is_valid_coord(row, col) \
                and self.is_cell_empty(row, col) \
                and player == self.current_player \
                and True in [self.has_piece_to_flip(row, col, direction) for direction in self.move_dirs]

    # Checks if the player's move can flip a piece in the given direction
    def has_piece_to_flip(self, row, col, direction) -> bool:
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
        return 0 <= row < self.size and 0 <= col < self.size

    # Gives turn to other player
    def swap_turns(self) -> None:
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    # Prints cell coordinates of all legal moves available to the current player
    def find_legal_moves(self):
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.is_move_legal(row, col, self.current_player):
                    moves.append([row, col])
        return moves

    # Restores the game's initial state
    def reset_game(self):
        self.board.set_up_board()
        self.current_player = self.player1
        self.update_scores()

    # Checks if the game is over, the game is over when no legal moves
    # remain for either player
    def game_over(self) -> bool:
        return not self.has_legal_move_remaining(self.player1) \
                and not self.has_legal_move_remaining(self.player2)

    # Returns the winning player, None if the game ends in draw
    def declare_winner(self) -> Player:
        scores = self.player_scores.values()

        # Handles draw
        if len(set(scores)) == 1:
            return None

        winning_score = max(self.player_scores.values())
        for player in self.get_players():
            if self.player_scores[player] == winning_score:
                return player

    # Stores the current state of the game
    def store_game_state(self):
        state = GameState(self.current_player, self.player_scores, self.board)
        self.state_history.append(state)

    # Loads game from saved game state
    def load_game_state(self, state: GameState):
        self.current_player = state.current_player
        self.player_scores = state.scores
        self.board = state.board

    # Updates both players' scores
    def update_scores(self) -> None:
        self.player_scores[self.player1] = 0
        self.player_scores[self.player2] = 0

        for row in range(self.size):
            for col in range(self.size):
                player = self.get_player_at_cell(row, col)
                if player:
                    self.player_scores[player] += 1

    #serializes game state to pass to store game state in database
    def serialize_game_state(self):
        game_state = {
            'current_player_symbol': color_to_symbol[self.get_current_player_color()],
            'board': [[color_to_symbol[cell] for cell in row] for row in self.board.get_board()],
            'player_scores':{color_to_symbol[self.player1.get_color()]: self.get_player_score(self.player1),
                             color_to_symbol[self.player2.get_color()]: self.get_player_score(self.player2)}
        }
        return json.dumps(game_state)

    #deserialize game state to reconstruct game from game state stored in database
    def deserialize_game_state(self, json_string):

        game_state = json.loads(json_string)
        board_size = len(game_state['board'])
        current_player_symbol = game_state['current_player_symbol']
        board_data = game_state['board']

        for player in self.get_players():
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
