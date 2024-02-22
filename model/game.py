from model.board import Board
from model.player_color import PlayerColor
from model.player_color import color_to_symbol
from model.player import Player

class Game:
    def __init__(self, size=8) -> None:
        self.player1 = Player(PlayerColor.Black)
        self.player2 = Player(PlayerColor.White)
        self.board = Board(size)
        self.size = self.board.get_size()
        self.current_player = self.player1
        self.player_scores = {self.player1: 2,
                              self.player2: 2}
        self.move_dirs = [(-1, -1), (-1, 0),
                          (-1, +1), (0, -1),
                          (0, +1), (+1, -1),
                          (+1, 0), (+1, +1)]

    # Returns the current player's color
    def get_current_player_color(self):
        return self.current_player.get_color()

    # Returns the current player
    def get_current_player(self):
        return self.current_player

    # Returns all players in the game
    def get_all_players(self):
        return [player for player in self.player_scores.keys()]

    # Executes move on the given cell coordinates if the move is legal
    # Allows reattempt if move is illegal
    def make_move(self, row, col):
        if self.is_move_legal(row, col, self.current_player):
            self.board.fill_cell(row, col, self.current_player.get_color())
            self.flip_pieces(row, col)
            self.update_scores()
            self.swap_turns()
            return True
        else:
            return False

    # Determines if this player a legal move left to play
    def has_legal_move_remaining(self, player: Player):
        for row in range(self.board.get_size()):
            for col in range(self.board.get_size()):
                if self.is_move_legal(row, col, player):
                    return True
        return False

    # Checks if the player's move is legal
    def is_move_legal(self, row, col, player: Player) -> bool:
        return self.is_valid_coord(row, col) \
                and self.board.is_cell_empty(row, col) \
                and player == self.current_player \
                and True in [self.has_piece_to_flip(row, col, direction) for direction in self.move_dirs]

    # Checks if the player's move can flip a piece in the given direction
    def has_piece_to_flip(self, row, col, direction) -> bool:
        start_x, start_y = row, col
        x, y = direction

        while self.is_valid_coord(row + x, col + y):
            # Disqualify this direction if the adjacent cell is empty
            if self.board.is_cell_empty(row + x, col + y):
                break
            # Disqualify this direction if the adjacent piece belongs to the curerent player
            if self.current_player.get_color() \
                    == self.board.get_cell(start_x + x, start_y + y):
                break
            # Return true if the current place has a non-adjacent piece in the given direction
            if self.current_player.get_color() \
                    == self.board.get_cell(row + x, col + y):
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
        board_size = self.board.get_size()
        return 0 <= row < board_size and 0 <= col < board_size

    # Gives turn to other player
    def swap_turns(self) -> None:
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    # Prints cell coordinates of all legal moves available to the current player
    def find_legal_moves(self) -> [int, int]:
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.is_move_legal(row, col, self.current_player):
                    moves.append([row, col])
        return moves

    # Checks if the game is over, the game is over when no legal moves
    # remain for either player
    def game_over(self) -> bool:
        return not self.has_legal_move_remaining(self.player1) \
                and not self.has_legal_move_remaining(self.player2)

    # Returns this player's score (number of pieces)
    def get_player_score(self, player: Player) -> int:
        return self.player_scores[player]

    # Returns the winning player, None if the game ends in draw
    def declare_winner(self) -> Player:
        scores = self.player_scores.values()
        # Handles draw
        if len(set(scores)) == 1:
            return None

        winning_score = max(self.player_scores.values())
        for player in self.player_scores.keys():
            if self.player_scores[player] == winning_score:
                return player

    # Updates both players' scores
    def update_scores(self) -> None:
        self.player_scores[self.player1] = 0
        self.player_scores[self.player2] = 0

        for row in range(self.board.get_size()):
            for col in range(self.board.get_size()):
                if self.board.get_cell(row, col) == self.player1.get_color():
                    self.player_scores[self.player1] += 1
                if self.board.get_cell(row, col) == self.player2.get_color():
                    self.player_scores[self.player2] += 1
