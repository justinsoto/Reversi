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
    def display_draw_message(self):
        pass

    @abstractmethod
    def display_score(self, player):
        pass

    @abstractmethod
    def display_legal_moves(self, player):
        pass

    @abstractmethod
    def display_legal_moves(self):
        pass

    @abstractmethod
    def display_final_scoreboard(self):
        pass

    @abstractmethod
    def get_move(self):
        pass
