from model.game import Game
from abc import ABC, abstractmethod
import random

class MoveStrategy(ABC):
    @abstractmethod
    def choose_move(self, game: Game):
        pass

class MinimaxStrategy(MoveStrategy):
    def __init__(self, depth):
        self.depth = depth

    def choose_move(self, game: Game):
        # add minimax logic later
        pass

class RandomStrategy(MoveStrategy):
    def choose_move(self, game: Game):
        # example of a simple strategy, selecting a move randomly
        possible_moves = game.get_possible_moves()
        if possible_moves:
            return random.choice(possible_moves)
        return None
