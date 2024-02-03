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
        self.board.make_move(row, col, self.current_player)

    