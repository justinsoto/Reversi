from abc import ABC, abstractmethod

class ConsoleBoardView(ABC):
    def __init__(self, game) -> None:
       pass

    @abstractmethod
    def __str__(self) -> str:
        pass
    
    @abstractmethod
    def display_current_player(self):
       pass

    @abstractmethod
    def display_illegal_move_message(self):
        pass

    @abstractmethod
    def display_winner(self, winner):
        pass

    @abstractmethod
    def display_draw_message(self):
        pass

    @abstractmethod
    def display_board(self):
        pass

    @abstractmethod
    def display_score(self, player):
         pass

    @abstractmethod
    def display_legal_moves(self):
        pass

    
    @abstractmethod
    def display_final_scorebaord(self):
        pass
