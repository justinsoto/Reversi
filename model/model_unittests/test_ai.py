import unittest
from model.ai import AI
from model.game import Game 
from model.ai_strategy import MoveStrategy


class MockStrategy(MoveStrategy):
    def choose_move(self):
        return (2, 3)  # Mocking a move tuple for testing

class TestAI(unittest.TestCase):
    def setUp(self):
        self.game = Game(8, "player1", "player2")
        self.strategy = MockStrategy(1,self.game)
        self.ai = AI(self.game, self.strategy)
    
    def test_choose_move(self):
        move = self.ai.choose_move()
        self.assertIsInstance(move, tuple)
        self.assertEqual(len(move), 2)
        self.assertIsInstance(move[0], int)
        self.assertIsInstance(move[1], int) 
        self.assertIn(move[0], range(8))
        self.assertIn(move[1], range(8))

        