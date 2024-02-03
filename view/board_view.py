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

    def show_curr_player(self, curr_player):
       print(f"It's {color_to_symbol[curr_player.color]}'s turn. ")

    def get_move(self):
        move = input('Enter your move (row, col): ')
        values = move.split(',')
        row, col = int(values[0]), int(values[1])
        return row, col

    def show_illegal_move(self, row, col):
        print('Illegal move. Try again.')

    def show_winner(self, player):
        print(f"Player {color_to_symbol[player.color]} won!")

    def show_draw(self):
        print('Game ended in a draw.')

    def display_board(self):
        print(self.game_board)
