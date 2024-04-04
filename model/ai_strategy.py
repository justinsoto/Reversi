from model.game import Game
from abc import ABC, abstractmethod
import random
import math
import copy

class MoveStrategy(ABC):
    def __init__(self, depth, game: Game):
        self.depth = depth
        self.game = game

    @abstractmethod
    def choose_move(self):
        pass

class MinimaxStrategy(MoveStrategy):
    def copy(self):
        new_game = Game(size=self.game.size)
        new_game.board = copy.deepcopy(self.game.board)
        new_game.player1 = copy.deepcopy(self.game.player1)
        new_game.player2 = copy.deepcopy(self.game.player2)
        new_game.current_player = self.game.current_player
        new_game.player_scores = copy.deepcopy(self.game.player_scores)
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
                game_copy = self.copy()
                game_copy.make_move(move[0], move[1])
                eval, _ = self.minimax(depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

    def choose_move(self):
        _, best_move = self.minimax(self.depth, True)
        return best_move

    def evaluate_board(self):
        num_legal_moves = len(self.game.find_legal_moves())

        score_diff = self.game.get_player_score(self.game.player2) - self.game.get_player_score(self.game.player1)

        corner_tiles = [(0, 0), (0, 7), (7, 0), (7, 7)]
        corner_count = sum(1 for tile in corner_tiles if self.game.board.board[tile[0]][tile[1]] == self.game.player2)

        edge_tiles = [(0, i) for i in range(1, 7)] + [(7, i) for i in range(1, 7)] + [(i, 0) for i in range(1, 7)] + [(i, 7) for i in range(1, 7)]
        edge_count = sum(1 for tile in edge_tiles if self.game.board.board[tile[0]][tile[1]] == self.game.player2)

        heuristic_score = num_legal_moves + score_diff + (10 * corner_count) + (5 * edge_count)

        return heuristic_score

class MiniMaxAlphaBeta(MoveStrategy):
    def copy(self):
        new_game = Game(size=self.game.size)
        new_game.board = copy.deepcopy(self.game.board)
        new_game.player1 = copy.deepcopy(self.game.player1)
        new_game.player2 = copy.deepcopy(self.game.player2)
        new_game.current_player = self.game.current_player
        new_game.player_scores = copy.deepcopy(self.game.player_scores)
        new_game.move_dirs = self.game.move_dirs[:]
        return new_game

    def minimaxAlphaBeta(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.game.game_over():
            return self.evaluate_board(), None

        if maximizing_player:
            max_eval = -math.inf
            best_move = None
            for move in self.game.find_legal_moves():
                game_copy = self.copy()
                game_copy.make_move(move[0], move[1])
                eval, _ = self.minimaxAlphaBeta(depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            best_move = None
            for move in self.game.find_legal_moves():
                game_copy = self.copy()
                game_copy.make_move(move[0], move[1])
                eval, _ = self.minimaxAlphaBeta(depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def choose_move(self):
        _, best_move = self.minimaxAlphaBeta(self.depth, -math.inf, math.inf, True)
        return best_move

    def evaluate_board(self):
        num_legal_moves = len(self.game.find_legal_moves())

        score_diff = self.game.get_player_score(self.game.player2) - self.game.get_player_score(self.game.player1)

        corner_tiles = [(0, 0), (0, 7), (7, 0), (7, 7)]
        corner_count = sum(1 for tile in corner_tiles if self.game.board.board[tile[0]][tile[1]] == self.game.player2)

        edge_tiles = [(0, i) for i in range(1, 7)] + [(7, i) for i in range(1, 7)] + [(i, 0) for i in range(1, 7)] + [(i, 7) for i in range(1, 7)]
        edge_count = sum(1 for tile in edge_tiles if self.game.board.board[tile[0]][tile[1]] == self.game.player2)

        heuristic_score = num_legal_moves + score_diff + (10 * corner_count) + (5 * edge_count)

        return heuristic_score

class RandomStrategy(MoveStrategy):
    def choose_move(self):
        # example of a simple strategy, selecting a move randomly
        possible_moves = self.game.find_legal_moves()
        if possible_moves:
            return random.choice(possible_moves)
        return None
