import unittest
from model.player import Player
from model.player_color import PlayerColor

class TestPlayer(unittest.TestCase):
    """
    Test suite for the Player class to verify functionality related to player attributes, such as color.
    """    
    def setUp(self):
        """
        Setup method to initialize two Player instances with different colors before each test.
        This helps in verifying that the Player instances handle attributes correctly.
        """        
        self.player1 = Player(PlayerColor.Black, 1)
        self.player2 = Player(PlayerColor.White, 2)
    
    def test_get_color(self):
        """
        Tests the get_color method of the Player class to ensure it returns the correct color associated with the player.
        This test checks for consistency in returning the assigned player colors.
        """        
        self.assertEqual(self.player1.get_color(), PlayerColor.Black)
        self.assertEqual(self.player2.get_color(), PlayerColor.White)