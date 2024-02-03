from abc import ABC, abstractmethod

class GameView(ABC):
    def __init__(self, board_view) -> None:
        self.board_view = board_view

    @abstractmethod
    def show_curr_player(self, curr_player):
        pass

    @abstractmethod
    def get_move(self):
        pass

    @abstractmethod
    def show_illegal_move(self, row, col):
        pass

    @abstractmethod
    def show_winner(self, player):
        pass

    @abstractmethod
    def show_draw(self):
        pass

    def display_board(self):
        self.board_view.display()

    

