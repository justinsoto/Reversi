import unittest
from model.player import Player
from model.player_color import PlayerColor

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player1 = Player(PlayerColor.Black, 1)
        self.player2 = Player(PlayerColor.White, 2)
    
    def test_get_color(self):
        self.assertEqual(self.player1.get_color(), PlayerColor.Black)
        self.assertEqual(self.player2.get_color(), PlayerColor.White)


