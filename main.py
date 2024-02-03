from model.board import Board
from view.board_view import BoardView
from model.game import Game

game = Game()
game.make_move(0, 0)
game.make_move(2, 3)
print(game)

