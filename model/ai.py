from model.game import Game
from model.ai_strategy import MoveStrategy

class AI():
    def __init__(self, game: Game, strategy: MoveStrategy):
        """
        Initializes the AI object with a specific game context and a decision-making strategy. This AI is 
        designed to interact with a game by making moves based on a predefined strategy.

        Parameters:
        game (Game): The current state of the game which the AI will interact with.
        strategy (MoveStrategy): The strategy object that defines how the AI decides on moves. The strategy 
        should be derived from the MoveStrategy abstract base class.
        """
        self.game = game
        self.strategy = strategy

    def choose_move(self):
        """
        Determines and returns the best move based on the strategy implemented by the AI.

        Returns:
        tuple: The best move as a tuple (row, column), determined by the strategy. The specifics of the move 
        (like its format and calculation) depend on the strategy's implementation of the choose_move method.
        """
        return self.strategy.choose_move()
