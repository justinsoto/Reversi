from model.player_color import PlayerColor
from model.player import Player

class Board:
    def __init__(self, size=8) -> None:
        """ Enforces specifications for the size of the board:
                - Must be minimum of 4x4
                - Must be (n x n) where n is even
        """

        if size < 4:
            self.size = 4
        elif size % 2 != 0:
            self.size = size + 1
        else:
            self.size = size

        self.curr_player = PlayerColor.Black
        self.num_tiles = [2, 2]
        self.board = []
        self.set_up_board()

    def set_up_board(self) -> None:
        self.board = [[PlayerColor.Empty for _ in range(self.size)] for _ in range(self.size)]
        center = self.size // 2

        self.board[center - 1][center - 1] = PlayerColor.Black
        self.board[center - 1][center] = PlayerColor.White
        self.board[center][center - 1] = PlayerColor.White
        self.board[center][center] = PlayerColor.Black

    def get_board(self):
        return self.board.copy()

    # def make_move(self, row, col, player: Player):
    #     self.board[row][col] = player.get_color()

    def get_cell(self, row, col) -> PlayerColor:
        return self.board[row][col] 

    def is_cell_empty(self, row, col) -> bool:
        return self.get_cell(row, col) == PlayerColor.Empty
    
    def fill_cell(self, row, col, color) -> None:
         self.board[row][col] = color

    def get_size(self) -> int:
        return self.size
    

    
