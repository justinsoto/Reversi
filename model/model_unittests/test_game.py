import unittest
from model.game import Game
from model.board import Board
from model.player import Player
from model.player_color import PlayerColor

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(8, "player1", "player2")

    def test_initialization(self):
        self.assertIsInstance(self.game.get_current_player(), Player)
        self.assertEqual(self.game.get_player_score(self.game.get_current_player()), 2)
        self.assertEqual(self.game.get_current_player_color(), PlayerColor.Black)
        self.assertEqual(self.game.get_board_size(), 8)

    def test_clone(self):
        clone = self.game.clone()
        self.assertIsInstance(clone, Game)
        serialized1 = self.game.serialize_game_state()
        serialized2 = clone.serialize_game_state()
        self.assertEqual(serialized1, serialized2)
    
    def test_get_board(self):
        board = self.game.get_board()
        self.assertIsInstance(board, Board)
        self.assertEqual(board.get_size(), 8)

    def test_get_current_player(self):
        current_player = self.game.get_current_player()
        self.assertIsInstance(current_player, Player)
        self.assertIn(current_player, self.game.get_all_players())

    def test_get_scores(self):
        scores = self.game.get_scores()
        self.assertIsInstance(scores, dict)
        self.assertEqual(len(scores), 2)
        self.assertIn(self.game.get_current_player(), scores.keys())

    
    def test_get_player_score(self):
        player = self.game.get_current_player()
        score = self.game.get_player_score(player)
        self.assertIsInstance(score, int)


    def test_get_current_player_color(self):
        color = self.game.get_current_player_color()
        self.assertIsInstance(color, PlayerColor)
        self.assertEqual(color, PlayerColor.Black)

    def test_get_board_size(self):
        size = self.game.get_board_size()
        self.assertIsInstance(size, int)
        self.assertEqual(size, 8)

    def test_get_all_players(self):
        players = self.game.get_all_players()
        self.assertIsInstance(players, list)
        self.assertEqual(len(players), 2)
        for player in players:
            self.assertIsInstance(player, Player)

    def test_get_player_at_cell(self):
        center = self.game.get_board_size() // 2
        player = self.game.get_player_at_cell(center-1, center-1)
        self.assertIsInstance(player, Player)
        self.assertEqual(player.get_color(), PlayerColor.White)


    def test_is_cell_empty(self):
        empty = self.game.is_cell_empty(0, 0)
        self.assertIsInstance(empty, bool)
        self.assertTrue(empty)

    def test_make_move(self):
        #has to be a legal move
        self.game.make_move(2, 3) #makes move and sets current player to white 
        player_at_cell = self.game.get_player_at_cell(2, 3) 
        self.assertFalse(self.game.is_cell_empty(2, 3))
        self.assertEqual(player_at_cell.get_color(), PlayerColor.Black)
        
    def test_has_legal_move_remaining(self):
        #current player is white
        self.assertTrue(self.game.has_legal_move_remaining(self.game.get_current_player())) 
        #set current player to black
        self.game.make_move(2, 2)
        self.assertTrue(self.game.has_legal_move_remaining(self.game.get_current_player()))
                        

    def test_is_move_legal(self):
      center = self.game.get_board_size() // 2
      self.assertFalse(self.game.is_move_legal(center-1, center-1, self.game.get_current_player()))
      #black should be current player
      self.assertTrue(self.game.is_move_legal(2, 3, self.game.get_current_player())) 



    def test_is_valid_coord(self):
        size = self.game.get_board_size()
        self.assertTrue(self.game.is_valid_coord(0, 0))
        self.assertTrue(self.game.is_valid_coord(size-1, size-1))
        self.assertFalse(self.game.is_valid_coord(size, size))
        self.assertFalse(self.game.is_valid_coord(-1, -1))
        

    def test_swap_turns(self):
        curr_player = self.game.get_current_player()
        self.game.swap_turns()
        self.assertNotEqual(curr_player, self.game.get_current_player())

    def test_find_legal_moves(self):
        legal_moves = self.game.find_legal_moves()
        self.assertIsInstance(legal_moves, list)
        for move in legal_moves:
            self.assertIsInstance(move, list)
            self.assertEqual(len(move), 2)
            self.assertTrue(self.game.is_move_legal(move[0], move[1], self.game.get_current_player()))

    def test_reset_game(self):
        make_move = self.game.make_move(2, 3) 
        self.assertFalse(self.game.is_cell_empty(2, 3))
        self.game.reset_game()
        self.assertTrue(self.game.is_cell_empty(2, 3))
        self.assertEqual(self.game.get_current_player_color(), PlayerColor.Black)
        self.assertEqual(self.game.get_player_score(self.game.get_current_player()), 2)




