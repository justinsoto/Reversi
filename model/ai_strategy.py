from model.game import Game
from abc import ABC, abstractmethod
import random
import math
from time import sleep
from model.player import Player

class MoveStrategy(ABC):
    def __init__(self, depth, game: Game):
        """
        Initializes the base MoveStrategy with a game instance and a specified search depth for AI calculations.

        Parameters:
        depth (int): The depth to which the AI will calculate moves ahead.
        game (Game): The current game instance which includes the game state.
        """        
        self.depth = depth
        self.game = game
        self.best_move = [0,0]
        self.scores = self.generate_scores(self.game.size)

    @abstractmethod
    def choose_move(self):
        """
        Abstract method to choose a move based on the strategy. To be implemented by subclasses.
        """        
        pass

    def generate_scores(self, size):
        """
        Generates a scoring grid based on proximity to the edges of the board, valuing corners and edges higher.

        Parameters:
        size (int): The size of the game board.

        Returns:
        list: A 2D list of scores corresponding to each cell on the board.
        """        
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
        """
        Implements the minimax algorithm to select the best move from the current game state.

        Returns:
        tuple: The row and column index of the best move as determined by the minimax algorithm.
        """        
        best_move = self.minimax(self.game, self.depth, self.game.player2)[0]
        return best_move

    def minimax(self, game: Game, depth, player: Player):
        """
        A recursive minimax algorithm that evaluates game positions to determine the best move.

        Parameters:
        game (Game): The game instance to evaluate.
        depth (int): The maximum depth to search.
        player (Player): The player whose move is being evaluated.

        Returns:
        tuple: The best move as a tuple and the score associated with that move.
        """        
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
        """
        Evaluates the current game state and returns a score based on the difference in disc count and corner control.

        Parameters:
        game (Game): The game instance to evaluate.

        Returns:
        int: The evaluated score of the current game state, favoring the player with more discs and corner control.
        """     
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
        """
        Determines the opponent of the current player.

        Parameters:
        player (Player): The current player.

        Returns:
        Player: The opponent player.
        """     
        if player == self.game.player1:
            return self.game.player2
        else:
            return self.game.player1

class MiniMaxAlphaBeta(MoveStrategy):
    def choose_move(self):
        """
        Chooses the best move using the minimax algorithm with alpha-beta pruning to enhance performance.

        Returns:
        tuple: The row and column index of the best move as determined by the minimax algorithm with alpha-beta pruning.
        """      
        best_move = self.minimax(self.game, self.depth, -math.inf, math.inf, self.game.player2)[0]
        return best_move

    def minimax(self, game: Game, depth, alpha, beta, player: Player):
        """
        A recursive minimax algorithm with alpha-beta pruning that evaluates game positions to determine the best move.

        Parameters:
        game (Game): The game instance to evaluate.
        depth (int): The maximum depth to search.
        alpha (float): The alpha value for alpha-beta pruning.
        beta (float): The beta value for alpha-beta pruning.
        player (Player): The player whose move is being evaluated.

        Returns:
        tuple: The best move as a tuple and the score associated with that move.
        """       
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
        """
        Evaluates the game state to provide a heuristic value for the minimax algorithm with alpha-beta pruning. 
        This evaluation considers both the differential in disc count between the current player and their opponent 
        and the control of corner squares, which are typically of strategic importance in games like Othello.

        Parameters:
        game (Game): The game instance to evaluate.

        Returns:
        int: The heuristic value of the board, calculated as the difference in scores adjusted for corner control.
        """

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
        """
        Determines the opponent of the specified player. This method is useful for switching between players 
        during the minimax algorithm's recursive exploration of game states.

        Parameters:
        player (Player): The player whose opponent is to be identified.

        Returns:
        Player: The opponent of the given player.
        """        
        if player == self.game.player1:
            return self.game.player2
        else:
            return self.game.player1


class RandomStrategy(MoveStrategy):
    def choose_move(self):
        """
        Selects a move randomly from the list of legal moves available in the current game state.

        Returns:
        tuple: The row and column index of a randomly selected move, or None if no moves are available.
        """        
        # example of a simple strategy, selecting a move randomly
        possible_moves = self.game.find_legal_moves()
        if possible_moves:
            move = random.choice(possible_moves)
            print(move)
            return move
        return None