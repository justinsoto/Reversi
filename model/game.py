from model.board import Board
from model.player_color import PlayerColor
from model.player import Player
from view.text_view import TextView

MOVE_DIRS = [(-1, -1), (-1, 0), (-1, +1),
             (0, -1),           (0, +1),
             (+1, -1), (+1, 0), (+1, +1)]

class Game:
    def __init__(self, size=8) -> None:
        self.player1 = Player(PlayerColor.Black)
        self.player2 = Player(PlayerColor.White)
        self.board = Board(size)
        self.current_player = self.player1

    def __str__(self) -> str:
        view = TextView(self.board)
        return view.__str__()

    def make_move(self, row, col):
        if self.is_legal_move([row, col]):
            self.board.board[row][col] = self.current_player.get_color()
            self.board.num_tiles[self.current_player.color - 1] += 1
            self.flip_tiles([row, col])
            self.switch_turns()

    def is_legal_move(self, move):
        #checks if the player's move is legal
        if self.is_valid_coord(move[0], move[1]) and self.board.board[move[0]][move[1]] == 0:
            for direction in MOVE_DIRS:
                if self.has_tile_to_flip(move, direction):
                    return True
        print("not legal move")
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
        for direction in MOVE_DIRS:
            if self.has_tile_to_flip(move, direction):
                i = 1
                while True:
                    row = move[0] + direction[0] * i
                    col = move[1] + direction[1] * i
                    if self.board.board[row][col] == curr_tile:
                        break
                    else:
                        self.board.board[row][col] = curr_tile
                        self.board.num_tiles[self.current_player.color] += 1
                        self.board.num_tiles[(self.current_player.color + 1) % 2] -= 1
                        i += 1

    def is_valid_coord(self, row, col):
        #checks if a move's coordinates are within board coordinates
        if 0 <= row < self.board.size and 0 <= col < self.board.size:
            return True
        return False

    def switch_turns(self):
        if self.current_player == self.player1:
            self.current_player == self.player2
        if self.current_player == self.player2:
            self.current_player == self.player1

    def has_legal_move(self):
        for row in range(self.board.size):
            for col in range(self.board.size):
                move = (row, col)
                if self.is_legal_move(move):
                    print("row: ", row)
                    print("column: ", col)
