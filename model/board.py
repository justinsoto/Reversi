from model.prototype import Prototype
from model.player_color import PlayerColor

class Board(Prototype):
    def __init__(self, size=8):
        """
        Initializes a new board for the game with a specified size, enforcing specific constraints:
        - The size must be at least 4x4 and at most 10x10.
        - The board dimensions must be even (n x n).

        Parameters:
        size (int, optional): The size of the board, which defaults to 8 if not specified.
        """
        if size < 4:
            self.size = 4

        if size > 10:
            self.size = 10

        if size % 2 != 0:
            self.size = size + 1
        else:
            self.size = size

        self.board = []
        self.set_up_board()

    def set_up_board(self) -> None:
        """
        Sets up the initial configuration of the game board, placing four pieces in the center in a standard
        starting pattern for games like Reversi.
        """        
        self.board = [[PlayerColor.Empty for _ in range(self.size)] for _ in range(self.size)]
        center = self.size // 2

        self.board[center - 1][center - 1] = PlayerColor.White
        self.board[center - 1][center] = PlayerColor.Black
        self.board[center][center - 1] = PlayerColor.Black
        self.board[center][center] = PlayerColor.White

    def get_board(self):
        """
        Retrieves a deep copy of the current board state.

        Returns:
        list: A nested list representing the current state of the board with each cell's color.
        """        
        return [[color for color in row] for row in self.board]

    def get_cell(self, row, col) -> PlayerColor:
        """
        Returns the color of the piece at the specified cell on the board.

        Parameters:
        row (int): The row index of the cell.
        col (int): The column index of the cell.

        Returns:
        PlayerColor: The color of the piece at the specified cell.
        """        
        return self.board[row][col]

    def is_cell_empty(self, row, col) -> bool:
        """
        Checks whether a specified cell is empty.

        Parameters:
        row (int): The row index of the cell.
        col (int): The column index of the cell.

        Returns:
        bool: True if the cell is empty, False otherwise.
        """        
        return self.get_cell(row, col) == PlayerColor.Empty

    def fill_cell(self, row, col, color) -> None:
        """
        Places a piece of a specified color in a specified cell on the board.

        Parameters:
        row (int): The row index of the cell where the piece will be placed.
        col (int): The column index of the cell where the piece will be placed.
        color (PlayerColor): The color of the piece to be placed.
        """         
        self.board[row][col] = color

    def get_size(self) -> int:
        """
        Returns the size of the board.

        Returns:
        int: The size of the board.
        """        
        return self.size
    
    def clone(self):
        """
        Creates a deep copy of the board instance, including its current state.

        Returns:
        Board: A new Board instance with the same size and pieces arranged in the same configuration.
        """        
        clone = Board(self.size)
        clone.board = self.get_board()
        return clone