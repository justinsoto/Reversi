import unittest
from model.board import Board
from model.player_color import PlayerColor

class TestBoard(unittest.TestCase):
    """
    Test suite for the Board class to verify functionality such as board setup, cell access,
    cell modification, and integrity of board cloning.
    """    
    def setUp(self):
        """
        Set up method to initialize a board instance with a default size before each test.
        """        
        self.board_size = 8
        self.board = Board(8)
        

    def test_set_up_board(self):
        """
        Verifies that the initial board setup places the correct colors in the central positions,
        following standard Othello/Reversi starting position rules.
        """        
        center = self.board_size // 2

        self.assertEqual(self.board.get_cell(center - 1, center - 1), PlayerColor.White)
        self.assertEqual(self.board.get_cell(center - 1, center), PlayerColor.Black)
        self.assertEqual(self.board.get_cell(center, center - 1), PlayerColor.Black)
        self.assertEqual(self.board.get_cell(center, center), PlayerColor.White)

    def test_get_board(self):
        """
        Tests that the get_board method returns a list of lists that represents the board,
        and that each cell contains a valid PlayerColor value.
        """        
        board = self.board.get_board()
        self.assertIsInstance(board, list)
        self.assertEqual(len(board), self.board_size)
        for row in board:
            self.assertIsInstance(row, list)
            self.assertEqual(len(row), self.board_size)
            for cell in row:
                self.assertIsInstance(cell, PlayerColor)

    def test_get_cell(self):
        """
        Tests the get_cell method to ensure it correctly retrieves the color of a specified cell
        and that the is_cell_empty and fill_cell methods correctly report and modify cell states.
        """        
        self.assertTrue(self.board.is_cell_empty(0, 0))
        self.board.fill_cell(0, 0, PlayerColor.White)
        self.assertEqual(self.board.get_cell(0, 0), PlayerColor.White) 

    def test_is_cell_empty(self):
        """
        Tests that is_cell_empty accurately identifies empty and filled cells.
        """        
        self.assertTrue(self.board.is_cell_empty(self.board_size - 1, self.board_size - 1))
        self.board.fill_cell(self.board_size - 1, self.board_size - 1, PlayerColor.Black)
        self.assertFalse(self.board.is_cell_empty(self.board_size - 1, self.board_size - 1))

    def test_fill_cell(self):
        """
        Verifies that fill_cell changes the state of a specified cell to the given PlayerColor.
        """        
        #find an empty cell
        row = 0
        col = 0
        while not self.board.is_cell_empty(row, col):
            col += 1
            if col == self.board_size:
                col = 0
                row += 1
        self.board.fill_cell(row, col, PlayerColor.Black)
        self.assertEqual(self.board.get_cell(row, col), PlayerColor.Black)

    def test_get_size(self):
        """
        Tests that get_size correctly returns the size of the board.
        """        
        self.assertEqual(self.board.get_size(), self.board_size)

    def test_clone(self):
        """
        Verifies that the clone method produces an exact copy of the board that is independent of the original.
        """        
        clone = self.board.clone()
        self.assertIsInstance(clone, Board)
        self.assertEqual(self.board.get_board(), clone.get_board())
        self.assertEqual(self.board.get_size(), clone.get_size())
        


