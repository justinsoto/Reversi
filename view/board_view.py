from abc import ABC, abstractmethod
from model.board import Board

class BoardView(ABC):
    def __init__(self, board: Board) -> None:
        self.board = board

    @abstractmethod
    def display(self):
        pass
        