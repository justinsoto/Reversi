from model.board import Board
from view.board_view import BoardView
from model.player_color import PlayerColor
from model.player import Player

class Game:
    def __init__(self, size=8) -> None:
        self.player1 = Player(PlayerColor.Black)
        self.player2 = Player(PlayerColor.White)
        self.board = Board(size)
        self.current_player = self.player1
        self.move_dirs = [(-1, -1), (-1, 0), 
                          (-1, +1), (0, -1),           
                          (0, +1), (+1, -1), 
                          (+1, 0), (+1, +1)]

    def __str__(self) -> str:
        view = BoardView(self.board)
        return view.__str__()

    def make_move(self, row, col):
        if self.is_legal_move(row, col):
            self.board.fill_cell(row, col, self.current_player.get_color())
            self.board.num_tiles[self.current_player.color - 1] += 1
            self.flip_tiles(row, col)
            self.swap_turns()

    def is_legal_move(self, move):
        #checks if the player's move is legal
        row, col = move
        if self.is_valid_coord(row, col) and self.board.is_cell_empty(row, col):
            for direction in self.move_dirs:
                if self.has_tile_to_flip(move, direction):
                    return True
        return False

    def has_tile_to_flip(self, move, direction):
        #checks if the player's move can flip a tile in any direction
        i = 1
        if self.is_valid_coord(move[0], move[1]):
            curr_tile = self.current_player.color
            while True:
                row = move[0] + direction[0] * i
                col = move[1] + direction[1] * i
                if not self.is_valid_coord(row, col) or self.board.board[row][col] == 0:
                    return False
                elif self.board.board[row][col] == curr_tile:
                    break
                else:
                    i += 1
        return i > 1

    def flip_tiles(self, move):
        #flips tiles based on current move
        curr_tile = self.current_player.color
        for direction in self.move_dirs:
            if self.has_tile_to_flip(move, direction):
                i = 1
                while True:
                    row = move[0] + direction[0] * i
                    col = move[1] + direction[1] * i
                    if self.board.board[row][col] == curr_tile:
                        break
                    else:
                        self.board.board[row][col] = curr_tile
                        self.board.num_tiles[self.current_player.color - 1] += 1
                        self.board.num_tiles[(self.current_player.color) % 2] -= 1
                        i += 1

    def is_valid_coord(self, row, col):
        #checks if a move's coordinates are within board coordinates
        if 0 <= row < self.board.get_size() and 0 <= col < self.board.get_size():
            return True
        return False

    def swap_turns(self) -> None:
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def print_legal_moves(self):
        print("Legal moves available:")
        for row in range(self.board.get_size()):
            for col in range(self.board.get_size()):
                move = (row, col)
                if self.is_legal_move(move):
                    print(f'(row, col): {row}, {col}')
