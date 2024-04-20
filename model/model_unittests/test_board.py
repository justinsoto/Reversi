import unittest
from model.board import Board
from model.player_color import PlayerColor

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board_size = 8
        self.board = Board(8)
        

    def test_set_up_board(self):
        center = self.board_size // 2

        self.assertEqual(self.board.get_cell(center - 1, center - 1), PlayerColor.White)
        self.assertEqual(self.board.get_cell(center - 1, center), PlayerColor.Black)
        self.assertEqual(self.board.get_cell(center, center - 1), PlayerColor.Black)
        self.assertEqual(self.board.get_cell(center, center), PlayerColor.White)

    def test_get_board(self):
        board = self.board.get_board()
        self.assertIsInstance(board, list)
        self.assertEqual(len(board), self.board_size)
        for row in board:
            self.assertIsInstance(row, list)
            self.assertEqual(len(row), self.board_size)
            for cell in row:
                self.assertIsInstance(cell, PlayerColor)

    def test_get_cell(self):
        self.assertTrue(self.board.is_cell_empty(0, 0))
        self.board.fill_cell(0, 0, PlayerColor.White)
        self.assertEqual(self.board.get_cell(0, 0), PlayerColor.White) 

    def test_is_cell_empty(self):
        self.assertTrue(self.board.is_cell_empty(self.board_size - 1, self.board_size - 1))
        self.board.fill_cell(self.board_size - 1, self.board_size - 1, PlayerColor.Black)
        self.assertFalse(self.board.is_cell_empty(self.board_size - 1, self.board_size - 1))

    def test_fill_cell(self):
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
        self.assertEqual(self.board.get_size(), self.board_size)

    def test_clone(self):
        clone = self.board.clone()
        self.assertIsInstance(clone, Board)
        self.assertEqual(self.board.get_board(), clone.get_board())
        self.assertEqual(self.board.get_size(), clone.get_size())
        


