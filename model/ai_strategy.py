from model.game import Game
from abc import ABC, abstractmethod
import random
import math
from time import sleep
from model.player import Player

class MoveStrategy(ABC):
    def __init__(self, depth, game: Game):
        self.depth = depth
        self.game = game
        self.best_move = [0,0]
        self.scores = self.generate_scores(self.game.size)

    @abstractmethod
    def choose_move(self):
        pass

    def generate_scores(self, size):
        array = [[0]*size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                min_dist = min(i, j, size - i - 1, size - j - 1)
                array[i][j] = size - min_dist - 1
        array[0][size - 1] = size
        array[size - 1][0] = size
        array[0][0] = size
        array[size - 1][size - 1] = size
        return array

class MinimaxStrategy(MoveStrategy):
    def choose_move(self):
        best_move = self.minimax(self.game, self.depth, self.game.player2)[0]
        return best_move

    def minimax(self, game: Game, depth, player: Player):
        # Base Case: Reached the end of the search or game is over
        if depth == 0 or game.game_over():
            return None, self.evaluate(game)

        # Find all legal moves for the current player
        legal_moves = game.find_legal_moves()

        # If no legal moves are available, forfeit the turn
        if not legal_moves:
            return None, self.evaluate(game, player) * (-1 if player.get_color() == self.game.player1.get_color() else 1)

        # Initialize best move and score
        best_move = None
        best_score =-math.inf if player.get_color() == self.game.player1.get_color() else math.inf

        # Simulate each legal move and perform minimax on the resulting game state
        for row, col in legal_moves:
            # Clone the current game state to avoid modifying the original game
            simulated_game = game.clone()
            simulated_game.make_move(row, col)
            # Get the score for the simulated game state from the opponent's perspective
            move_score = self.minimax(simulated_game, depth - 1, self.get_opponent(player))[1]

            # Update best move and score based on the player's turn
            if player.get_color() == "Black":
                if move_score > best_score:
                    best_move = (row, col)
                    best_score = move_score
            else:
                if move_score < best_score:
                    best_move = (row, col)
                    best_score = move_score

        return best_move, best_score

    def evaluate(self, game: Game):
        # Calculate the difference in disc count between the player and their opponent
        game.swap_turns()
        if game.current_player.get_color() == game.player2:
            player = game.player2
            opponent = game.player1
        else:
            player = game.player1
            opponent = game.player2

        player_score_diff = game.get_player_score(player) - game.get_player_score(opponent)
        # Prioritize corner placement
        corner_count = 0
        board_size = game.get_board_size()
        for row in [0, board_size - 1]:
            for col in [0, board_size - 1]:
                if game.get_player_at_cell(row, col) == player:
                    corner_count += 1

        return player_score_diff + (1 * corner_count)

    def get_opponent(self, player: Player):
        if player == self.game.player1:
            return self.game.player2
        else:
            return self.game.player1

class MiniMaxAlphaBeta(MoveStrategy):
    def choose_move(self):
        best_move = self.minimax(self.game, self.depth, -math.inf, math.inf, self.game.player2)[0]
        return best_move

    def minimax(self, game: Game, depth, alpha, beta, player: Player):
        # Base Case: Reached the end of the search or game is over
        if depth == 0 or game.game_over():
            return None, self.evaluate(game)

        legal_moves = game.find_legal_moves()
        if not legal_moves:
            return None, self.evaluate(game, player) * (-1 if player.get_color() == self.game.player1.get_color() else 1)

        best_move = [0, 0]

        # Maximizing player (Black)
        if player.get_color() == "Black":
            best_score = -math.inf
            for row, col in legal_moves:
                simulated_game = game.clone()
                simulated_game.make_move(row, col)
                move_score = self.minimax(simulated_game, depth - 1, alpha, beta, self.get_opponent(player))[1]
                if move_score > best_score:
                    best_move = (row, col)
                    best_score = move_score
                alpha = max(alpha, best_score)  # Update alpha
                # Prune if beta is less than or equal to alpha (opponent cannot improve)
                if beta <= alpha:
                    break

        # Minimizing player (White)
        else:
            best_score = math.inf
            for row, col in legal_moves:
                simulated_game = game.clone()
                simulated_game.make_move(row, col)
                move_score = self.minimax(simulated_game, depth - 1, alpha, beta, self.get_opponent(player))[1]
                if move_score < best_score:
                    best_move = (row, col)
                    best_score = move_score
                beta = min(beta, best_score)  # Update beta
                # Prune if alpha is greater than or equal to beta (we can guarantee better)
                if alpha >= beta:
                    break

        return best_move, best_score

    def evaluate(self, game: Game):
        # Calculate the difference in disc count between the player and their opponent
        game.swap_turns()
        if game.current_player.get_color() == game.player2:
            player = game.player2
            opponent = game.player1
        else:
            player = game.player1
            opponent = game.player2

        player_score_diff = game.get_player_score(player) - game.get_player_score(opponent)
        # Prioritize corner placement
        corner_count = 0
        board_size = game.get_board_size()
        for row in [0, board_size - 1]:
            for col in [0, board_size - 1]:
                if game.get_player_at_cell(row, col) == player:
                    corner_count += 1

        return player_score_diff + (1 * corner_count)

    def get_opponent(self, player: Player):
        if player == self.game.player1:
            return self.game.player2
        else:
            return self.game.player1


class RandomStrategy(MoveStrategy):
    def choose_move(self):
        # example of a simple strategy, selecting a move randomly
        possible_moves = self.game.find_legal_moves()
        sleep(1)
        if possible_moves:
            move = random.choice(possible_moves)
            print(move)
            return move
        return None
