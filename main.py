from model.game import Game
from view.board_view import BoardView
from controller.controller import GameController
game = Game(4)
view = BoardView(game)
controller = GameController (game,view)
view.display_board()
controller.start_game()
