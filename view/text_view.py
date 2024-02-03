from model.board import Board
from model.player_color import color_to_symbol

class TextView:
    def __init__(self, game_board: Board) -> None:
        self.game_board = game_board

    def __str__(self) -> str:
        game_string = ''
        for row in self.game_board:
            for piece in row:
                game_string += ' ' + color_to_symbol[piece] + ' '
            game_string += '\n'
        return game_string

