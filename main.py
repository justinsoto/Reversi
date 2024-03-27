from model.game import Game
from view.console_items.console_game_view import ConsoleGameView
from controller.controller import GameController

size = 8
game = Game(size)
view = ConsoleGameView(game, size)
controller = GameController(game,view)
controller.start_game()
