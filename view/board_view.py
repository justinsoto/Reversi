from model.board import Board
from model.player_color import color_to_symbol

class BoardView:
    def __init__(self, game_board: Board) -> None:
        self.game_board = game_board

    def __str__(self) -> str:
        # Creates text-based version of the game 
        game_string = ''
        for row in self.game_board.get_board():
            for piece in row:
                game_string += ' ' + color_to_symbol[piece] + ' '
            game_string += '\n'
        return game_string

