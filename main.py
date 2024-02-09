from model.game import Game
from view.console_game_view import ConsoleGameView
from controller.controller import GameController

game = Game(8)
view = ConsoleGameView(game)
controller = GameController(game,view)
controller.start_game()
