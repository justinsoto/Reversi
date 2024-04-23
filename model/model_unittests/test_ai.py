import unittest
from model.ai import AI
from model.game import Game 
from model.ai_strategy import MoveStrategy

class MockStrategy(MoveStrategy):
    """
    A mock strategy class that simulates an AI strategy by always returning a predetermined move.
    This is used to isolate the AI class functionality from the strategy logic in unit tests.
    """    
    def choose_move(self):
        """
        Overrides the choose_move method to return a fixed move position, simplifying the testing of the AI class.

        Returns:
        tuple: A tuple representing a predetermined board position.
        """        
        return (2, 3)  # Mocking a move tuple for testing

class TestAI(unittest.TestCase):
    """
    Test suite for the AI class to ensure that it properly utilizes its strategy component to determine moves.
    """    
    def setUp(self):
        """
        Set up method to initialize resources before each test. It prepares a game instance, 
        a mock strategy instance, and an AI instance using these.
        """        
        self.game = Game(8, "player1", "player2")
        self.strategy = MockStrategy(1,self.game)
        self.ai = AI(self.game, self.strategy)
    
    def test_choose_move(self):
        """
        Tests the choose_move method of the AI class to ensure it correctly uses its strategy to obtain a move.
        This test verifies that the move returned is a tuple of integers representing valid board positions.
        """        
        move = self.ai.choose_move()
        self.assertIsInstance(move, tuple, "The move should be returned as a tuple.")
        self.assertEqual(len(move), 2, "The move should consist of two elements (row, col).")
        self.assertIsInstance(move[0], int, "The row component of the move should be an integer.")
        self.assertIsInstance(move[1], int, "The column component of the move should be an integer.")
        self.assertIn(move[0], range(8), "The row component should be within the valid range of the board.")
        self.assertIn(move[1], range(8), "The column component should be within the valid range of the board.")


        