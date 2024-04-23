import unittest
from model.game import Game
from model.board import Board
from model.player import Player
from model.player_color import PlayerColor

class TestGame(unittest.TestCase):
    """
    Test suite for the Game class to verify the functionality such as initialization, game state management,
    player and board interactions, and game logic.
    """    
    def setUp(self):
        """
        Setup method to initialize a game instance before each test. This game is configured with a standard
        8x8 board and two players.
        """        
        self.game = Game(8, "player1", "player2")

    def test_initialization(self):
        """
        Tests the initial state of the game to ensure that it starts with the correct settings including
        current player set to black, initial score, and board size.
        """        
        self.assertIsInstance(self.game.get_current_player(), Player)
        self.assertEqual(self.game.get_player_score(self.game.get_current_player()), 2)
        self.assertEqual(self.game.get_current_player_color(), PlayerColor.Black)
        self.assertEqual(self.game.get_board_size(), 8)

    def test_clone(self):
        """
        Tests the cloning functionality to ensure that a deep copy of the game state is correctly created.
        """        
        clone = self.game.clone()
        self.assertIsInstance(clone, Game)
        serialized1 = self.game.serialize_game_state()
        serialized2 = clone.serialize_game_state()
        self.assertEqual(serialized1, serialized2)
    
    def test_get_board(self):
        """
        Verifies that the get_board method returns a Board instance and its size is correct.
        """        
        board = self.game.get_board()
        self.assertIsInstance(board, Board)
        self.assertEqual(board.get_size(), 8)

    def test_get_current_player(self):
        """
        Tests retrieval of the current player and checks if they are correctly listed as a game participant.
        """        
        current_player = self.game.get_current_player()
        self.assertIsInstance(current_player, Player)
        self.assertIn(current_player, self.game.get_all_players())

    def test_get_scores(self):
        """
        Checks if the game's scorekeeping is correct and includes scores for all players.
        """        
        scores = self.game.get_scores()
        self.assertIsInstance(scores, dict)
        self.assertEqual(len(scores), 2)
        self.assertIn(self.game.get_current_player(), scores.keys())

    
    def test_get_player_score(self):
        """
        Tests the retrieval of a player's score to verify correctness and data type.
        """        
        player = self.game.get_current_player()
        score = self.game.get_player_score(player)
        self.assertIsInstance(score, int)


    def test_get_current_player_color(self):
        """
        Verifies that the current player's color is retrieved correctly and matches the expected value.
        """        
        color = self.game.get_current_player_color()
        self.assertIsInstance(color, PlayerColor)
        self.assertEqual(color, PlayerColor.Black)

    def test_get_board_size(self):
        """
        Ensures the game reports its board size correctly.
        """        
        size = self.game.get_board_size()
        self.assertIsInstance(size, int)
        self.assertEqual(size, 8)

    def test_get_all_players(self):
        """
        Tests retrieval of all game participants, ensuring the list contains the correct player objects.
        """        
        players = self.game.get_all_players()
        self.assertIsInstance(players, list)
        self.assertEqual(len(players), 2)
        for player in players:
            self.assertIsInstance(player, Player)

    def test_get_player_at_cell(self):
        """
        Verifies that the correct player is identified in a specific board cell post-initial setup.
        """        
        center = self.game.get_board_size() // 2
        player = self.game.get_player_at_cell(center-1, center-1)
        self.assertIsInstance(player, Player)
        self.assertEqual(player.get_color(), PlayerColor.White)


    def test_is_cell_empty(self):
        """
        Tests whether a cell at a specified location is empty at the start of the game.
        """        
        empty = self.game.is_cell_empty(0, 0)
        self.assertIsInstance(empty, bool)
        self.assertTrue(empty)

    def test_make_move(self):
        """
        Tests the make_move function to ensure it correctly updates the board and player state after a move.
        """        
        #has to be a legal move
        self.game.make_move(2, 3) #makes move and sets current player to white 
        player_at_cell = self.game.get_player_at_cell(2, 3) 
        self.assertFalse(self.game.is_cell_empty(2, 3))
        self.assertEqual(player_at_cell.get_color(), PlayerColor.Black)
        
    def test_has_legal_move_remaining(self):
        """
        Verifies that the game correctly determines if the current player has any legal moves remaining.
        """        
        #current player is white
        self.assertTrue(self.game.has_legal_move_remaining(self.game.get_current_player())) 
        #set current player to black
        self.game.make_move(2, 2)
        self.assertTrue(self.game.has_legal_move_remaining(self.game.get_current_player()))
                        

    def test_is_move_legal(self):
        """
        Tests the legality of a move based on current player and board state.
        """      
      center = self.game.get_board_size() // 2
      self.assertFalse(self.game.is_move_legal(center-1, center-1, self.game.get_current_player()))
      #black should be current player
      self.assertTrue(self.game.is_move_legal(2, 3, self.game.get_current_player())) 



    def test_is_valid_coord(self):
        """
        Tests whether the coordinates provided are within the valid range of the board dimensions.
        """        
        size = self.game.get_board_size()
        self.assertTrue(self.game.is_valid_coord(0, 0))
        self.assertTrue(self.game.is_valid_coord(size-1, size-1))
        self.assertFalse(self.game.is_valid_coord(size, size))
        self.assertFalse(self.game.is_valid_coord(-1, -1))
        

    def test_swap_turns(self):
        """
        Tests the functionality of switching the current player between the two players.
        """        
        curr_player = self.game.get_current_player()
        self.game.swap_turns()
        self.assertNotEqual(curr_player, self.game.get_current_player())

    def test_find_legal_moves(self):
        """
        Tests that the game can correctly identify all legal moves available to the current player.
        """        
        legal_moves = self.game.find_legal_moves()
        self.assertIsInstance(legal_moves, list)
        for move in legal_moves:
            self.assertIsInstance(move, list)
            self.assertEqual(len(move), 2)
            self.assertTrue(self.game.is_move_legal(move[0], move[1], self.game.get_current_player()))

    def test_reset_game(self):
        """
        Verifies that the reset_game function correctly resets the game to its initial state.
        """        
        make_move = self.game.make_move(2, 3) 
        self.assertFalse(self.game.is_cell_empty(2, 3))
        self.game.reset_game()
        self.assertTrue(self.game.is_cell_empty(2, 3))
        self.assertEqual(self.game.get_current_player_color(), PlayerColor.Black)
        self.assertEqual(self.game.get_player_score(self.game.get_current_player()), 2)