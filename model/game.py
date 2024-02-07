from model.board import Board
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

    # def __str__(self) -> str:
    #     view = BoardView(self.board)
    #     return view.__str__()
    
    def get_current_player_color(self):
        return self.current_player.get_color()

    def make_move(self, row, col):
        if self.is_move_legal(row, col, self.current_player):
            self.board.fill_cell(row, col, self.current_player.get_color())
            self.board.num_tiles[self.current_player.get_color() - 1] += 1
            self.flip_tiles(row, col)
            self.swap_turns()

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
                and True in [self.has_tile_to_flip(row, col, direction) for direction in self.move_dirs]

    # Checks if the player's move can flip a tile in the given direction
    def has_tile_to_flip(self, row, col, direction) -> bool:
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
            if self.current_player.get_color() \
                    == self.board.get_cell(row + x, col + y):
                return True
            row += x
            col += y

        return False 

        # i = 1
        # if self.is_valid_coord(row, col):
        #     curr_tile = self.current_player.get_color()
        #     while True:
        #         row = row + direction[0] * i
        #         col = col + direction[1] * i
        #         if self.board.is_cell_empty(row, col):
        #             return False
        #         elif self.board.get_cell(row, col) == curr_tile:
        #             break
        #         else:
        #             i += 1
        # return i > 1
    
    # Flips tiles based on current move
    def flip_tiles(self, row, col) -> None:
        curr_tile = self.current_player.get_color()
        start_x, start_y = row, col
        for direction in self.move_dirs:
            x, y = direction
            row, col = start_x, start_y
            if self.has_tile_to_flip(row, col, direction):
                print(direction)
                while self.is_valid_coord(row + x, col + y):
                    row += x
                    col += y
                    if self.board.get_cell(row, col) == curr_tile:
                        break
                    else:
                        self.board.fill_cell(row, col, curr_tile)
                        self.board.num_tiles[self.current_player.color - 1] += 1
                        self.board.num_tiles[(self.current_player.color) % 2] -= 1

    # Checks if a move's coordinates are within board coordinates
    def is_valid_coord(self, row, col):
        board_size = self.board.get_size()
        return 0 <= row < board_size and 0 <= col < board_size

    def swap_turns(self) -> None:
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def print_legal_moves(self):
        print("Legal moves available:")
        for row in range(self.board.get_size()):
            for col in range(self.board.get_size()):
                if self.is_move_legal(row, col, self.current_player):
                    print(f'(row, col): {row}, {col}')

    def game_over(self) -> bool:
        return not self.has_legal_move_remaining(self.player1) \
                and not self.has_legal_move_remaining(self.player2)
    
    def get_player_score(self, player: Player):
        player1_score, player2_score = self.board.get_scores
        if player == self.player1:
            return player1_score
        else:
            return player2_score
        
    def declare_winner(self) -> None:
        if self.get_player_score(self.player1) > self.get_player_score(self.player2):
            self.winner = self.player1
        else:
            self.winner = self.player2
        
    def print_winner(self) -> None:
        print(f'Winner: {self.winner} {max(self.get_player_score(self.player1), self.get_player_score(self.player2))} points')

    
