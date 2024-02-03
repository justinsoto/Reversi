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

        self.current_player = PlayerColor.Black
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
    
    def make_move(self, row, col, player: Player):
        self.board[row][col] = player.get_color()
        

        

