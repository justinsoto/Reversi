from abc import ABC, abstractmethod

class BoardView(ABC):
    def __init__(self) -> None:
       pass

    @abstractmethod
    def display_board(self):
        pass