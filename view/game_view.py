from abc import ABC, abstractmethod

class GameView(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def display_current_player(self):
        pass

    @abstractmethod
    def display_illegal_move_message(self, row, col):
        pass

    @abstractmethod
    def display_winner(self):
        pass
    
    @abstractmethod
    def display_board(self):
        pass

    @abstractmethod
    def display_draw_message(self):
        pass

    

