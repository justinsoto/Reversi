from model.game import Game
import math
import copy

class ai():
    def __init__(self, game: Game, depth):
        """
        Initializes the AI with the given game instance and depth for the minimax algorithm.

        Parameters:
        - game (Game): An instance of the Game class representing the current game state.
        - depth (int): The depth limit for the minimax algorithm, determining how many moves ahead the AI will consider.
        """
        self.game = game
        self.depth = depth

    def copy(self):
        """
        Creates a deep copy of the current game state.

        Returns:
        - Game: A deep copy of the current game state.
        """
        new_game = Game(size=self.game.size)
        new_game.board = copy.deepcopy(self.game.board)
        new_game.player1 = copy.deepcopy(self.game.player1)
        new_game.player2 = copy.deepcopy(self.game.player2)
        new_game.current_player = self.game.current_player
        new_game.player_scores = copy.deepcopy(self.game.player_scores)
        new_game.move_dirs = self.game.move_dirs[:]
        return new_game

    def minimax(self, depth, maximizing_player):
        """
        Implements the minimax algorithm to determine the best move for the AI.

        Parameters:
        - depth (int): The current depth in the game tree.
        - maximizing_player (bool): Indicates whether the current player is maximizing (True) or minimizing (False) their score.

        Returns:
        - tuple: A tuple containing the evaluation score and the corresponding best move.
        """
        if depth == 0 or self.game.game_over():
            return self.evaluate_board(), None

        if maximizing_player:
            max_eval = -math.inf
            best_move = None
            for move in self.game.find_legal_moves():
                game_copy = self.copy()
                game_copy.make_move(move[0], move[1])
                eval, _ = self.minimax(depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = math.inf
            best_move = None
            for move in self.game.find_legal_moves():
                game_copy = self.copy()
                game_copy.make_move(move[0], move[1])
                eval, _ = self.minimax(depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

    def get_best_move(self):
        """
        Determines the best move for the AI using the minimax algorithm.

        Returns:
        - tuple: The best move determined by the minimax algorithm.
        """
        _, best_move = self.minimax(self.depth, True)
        return best_move

    def evaluate_board(self):
        """
        Evaluates the current game state using a heuristic function.

        Returns:
        - int: The heuristic score representing the AI's evaluation of the current game state.
        """
        num_legal_moves = len(self.game.find_legal_moves())

        score_diff = self.game.get_player_score(self.game.player2) - self.game.get_player_score(self.game.player1)

        corner_tiles = [(0, 0), (0, 7), (7, 0), (7, 7)]
        corner_count = sum(1 for tile in corner_tiles if self.game.board.board[tile[0]][tile[1]] == self.game.player2)

        edge_tiles = [(0, i) for i in range(1, 7)] + [(7, i) for i in range(1, 7)] + [(i, 0) for i in range(1, 7)] + [(i, 7) for i in range(1, 7)]
        edge_count = sum(1 for tile in edge_tiles if self.game.board.board[tile[0]][tile[1]] == self.game.player2)

        heuristic_score = num_legal_moves + score_diff + (10 * corner_count) + (5 * edge_count)

        return heuristic_score
