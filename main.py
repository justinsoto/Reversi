from model.game import Game
from view.console_game_view import ConsoleBoardView
from controller.controller import GameController

game = Game(4)
#this will need to be game view not board view
view = ConsoleBoardView(game)
controller = GameController(game,view)
controller.start_game()