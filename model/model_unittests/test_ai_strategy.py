import unittest
from unittest.mock import patch
from model.game import Game
from model.ai_strategy import MoveStrategy, MinimaxStrategy, MiniMaxAlphaBeta, RandomStrategy
from model.player import Player

class TestMiniMaxStrategy(unittest.TestCase):
    """
    Unit tests for the MinimaxStrategy class to ensure it correctly computes the best move from a given game state.
    """    
    def setUp(self):
        """
        Setup method to initialize a game and the MinimaxStrategy before each test.
        """        
        self.game = Game(8, "player1", "player2")
        self.strategy = MinimaxStrategy(1, self.game)
        
    
    def test_choose_move(self):
        """
        Tests that the choose_move method of MinimaxStrategy returns a valid move within the bounds of the board.
        """        
        move = self.strategy.choose_move()
        self.assertIsInstance(move, tuple)
        self.assertEqual(len(move), 2)
        self.assertIsInstance(move[0], int)
        self.assertIsInstance(move[1], int) 
        self.assertIn(move[0], range(8))
        self.assertIn(move[1], range(8))

class TestMiniMaxAlphaBeta(unittest.TestCase):
    """
    Unit tests for the MiniMaxAlphaBeta class to ensure it correctly computes the best move using alpha-beta pruning.
    """    
    def setUp(self):
        """
        Setup method to initialize a game and the MiniMaxAlphaBeta strategy before each test.
        """        
        self.game = Game(8, "player1", "player2")
        self.strategy = MiniMaxAlphaBeta(1, self.game)
        
    
    def test_choose_move(self):
        """
        Tests that the choose_move method of MiniMaxAlphaBeta returns a valid move within the bounds of the board.
        """        
        move = self.strategy.choose_move()
        self.assertIsInstance(move, tuple)
        self.assertEqual(len(move), 2)
        self.assertIsInstance(move[0], int)
        self.assertIsInstance(move[1], int) 
        self.assertIn(move[0], range(8))
        self.assertIn(move[1], range(8))

class TestRandomStrategy(unittest.TestCase):
    """
    Unit tests for the RandomStrategy class to verify that it selects a valid random move from the available legal moves.
    """    
    def setUp(self):
        """
        Setup method to initialize a game and the RandomStrategy before each test.
        """        
        self.game = Game(8, "player1", "player2")
        self.strategy = RandomStrategy(1, self.game)
        
    
    def test_choose_move(self):
        """
        Tests that the choose_move method of RandomStrategy returns a valid move that is within the bounds of the board.
        """        
        move = self.strategy.choose_move()
        self.assertIsInstance(move, list)
        self.assertEqual(len(move), 2)
        self.assertIsInstance(move[0], int)
        self.assertIsInstance(move[1], int) 
        self.assertIn(move[0], range(8))
        self.assertIn(move[1], range(8))
