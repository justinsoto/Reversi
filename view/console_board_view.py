from model.player import Player
from model.player_color import color_to_symbol
from model.game import Game

class ConsoleBoardView():
    def __init__(self, game: Game):
        self.board = game.board

    def __str__(self) -> str:
        # Creates text-based version of the game
        game_string = ''
        for row in self.game_board.get_board():
            for piece in row:
                game_string += ' ' + color_to_symbol[piece] + ' '
            game_string += '\n'
        return game_string
