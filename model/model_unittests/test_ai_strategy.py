import unittest
from unittest.mock import patch
from model.game import Game
from model.ai_strategy import MoveStrategy, MinimaxStrategy, MiniMaxAlphaBeta, RandomStrategy
from model.player import Player

class TestMiniMaxStrategy(unittest.TestCase):
    def setUp(self):
        self.game = Game(8, "player1", "player2")
        self.strategy = MinimaxStrategy(1, self.game)
        
    
    def test_choose_move(self):
        move = self.strategy.choose_move()
        self.assertIsInstance(move, tuple)
        self.assertEqual(len(move), 2)
        self.assertIsInstance(move[0], int)
        self.assertIsInstance(move[1], int) 
        self.assertIn(move[0], range(8))
        self.assertIn(move[1], range(8))

class TestMiniMaxAlphaBeta(unittest.TestCase):
    def setUp(self):
        self.game = Game(8, "player1", "player2")
        self.strategy = MiniMaxAlphaBeta(1, self.game)
        
    
    def test_choose_move(self):
        move = self.strategy.choose_move()
        self.assertIsInstance(move, tuple)
        self.assertEqual(len(move), 2)
        self.assertIsInstance(move[0], int)
        self.assertIsInstance(move[1], int) 
        self.assertIn(move[0], range(8))
        self.assertIn(move[1], range(8))

class TestRandomStrategy(unittest.TestCase):
    def setUp(self):
        self.game = Game(8, "player1", "player2")
        self.strategy = RandomStrategy(1, self.game)
        
    
    def test_choose_move(self):
        move = self.strategy.choose_move()
        self.assertIsInstance(move, list)
        self.assertEqual(len(move), 2)
        self.assertIsInstance(move[0], int)
        self.assertIsInstance(move[1], int) 
        self.assertIn(move[0], range(8))
        self.assertIn(move[1], range(8))
