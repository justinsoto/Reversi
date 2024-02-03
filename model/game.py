from model.board import Board
from model.player_color import PlayerColor
from model.player import Player
from view.board_view import BoardView

class Game:
    def __init__(self, size=8) -> None:
        self.player1 = Player(PlayerColor.Black)
        self.player2 = Player(PlayerColor.White)
        self.board = Board(size)
        self.current_player = self.player1

    def __str__(self) -> str:
        view = BoardView(self.board)
        return view.__str__()

    def make_move(self, row, col):
        # Check if space is empty 
        if not self.board.is_cell_empty(row, col):
            print("Taken cell. Try again.\n")
            
        # Check if move is legal 
        self.board.make_move(row, col, self.current_player)

    # Gives turn to the opposite player
    def swap_turns(self) -> None:
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    