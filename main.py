from model.game import Game
from view.test_board_view import BoardView
from controller.controller import GameController

game = Game(8)
view = BoardView(game)
controller = GameController(game,view)
controller.start_game()
