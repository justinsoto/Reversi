from model.board import Board
from model.player_color import color_to_symbol

class ConsoleBoardView():
    def __init__(self, board: Board):
        self.board = board

    # Creates text-based version of the game
    def __str__(self) -> str:
        game_string = ''
        for row in self.board.get_board():
            for piece in row:
                game_string += ' ' + color_to_symbol[piece] + ' '
            game_string += '\n'
        return game_string
