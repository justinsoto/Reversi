from model.game import Game
from model.ai_strategy import MoveStrategy

class AI():
    def __init__(self, game: Game, strategy: MoveStrategy):
        """
        Initializes the AI with the given game instance and strategy for making decisions.
        - game (Game): An instance of the Game class representing the current game state.
        - strategy (MoveStrategy): The strategy for choosing moves.
        """
        self.game = game
        self.strategy = strategy

    def choose_move(self):
        """
        determines the best move for the AI using the chosen strategy.
        returns:
        - the best move determined by the strategy.
        """
        return self.strategy.choose_move()
