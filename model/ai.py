from model.game import Game
import math
import copy

class ai():
    def __init__(self, game: Game, depth):
        self.game = game
        self.depth = depth

    def copy(self):
        # Create a new instance of the Game class
        new_game = Game(size=self.game.size)

        # Copy the board state
        new_game.board = copy.deepcopy(self.game.board)

        # Copy player attributes
        new_game.player1 = copy.deepcopy(self.game.player1)
        new_game.player2 = copy.deepcopy(self.game.player2)

        # Copy current player
        new_game.current_player = self.game.current_player

        # Copy player scores
        new_game.player_scores = copy.deepcopy(self.game.player_scores)

        # Copy move directions
        new_game.move_dirs = self.game.move_dirs[:]

        return new_game

    def minimax(self, depth, maximizing_player):
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
                game_copy = self.copy()  # Create a copy of the game state
                game_copy.make_move(move[0], move[1])
                eval, _ = self.minimax(depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

    def get_best_move(self):
        _, best_move = self.minimax(self.depth, True)
        return best_move

    def evaluate_board(self):
        # You can implement your own heuristic evaluation function here
        # For simplicity, let's just return the difference between AI's score and opponent's score
        ai_score = self.game.get_player_score(self.game.player2)
        opponent_score = self.game.get_player_score(self.game.player1)
        return ai_score - opponent_score
