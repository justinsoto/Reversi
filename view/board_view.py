from model.game import Game
from view.game_view import GameView
from model.board import Board
from model.player_color import color_to_symbol

class BoardView(GameView):
    def __init__(self, game: Game) -> None:
        super.__init__()
        self.game = game
        self.game_board = game.board

    def __str__(self) -> str:
        # Creates text-based version of the game
        game_string = ''
        for row in self.game_board.get_board():
            for piece in row:
                game_string += ' ' + color_to_symbol[piece] + ' '
            game_string += '\n'
        return game_string

    def display_current_player(self):
       curr_player = self.game.get_current_player_color()
       print(f"It's {color_to_symbol[curr_player]}'s turn. ")

    def get_move(self):
        move = input('Enter your move (row, col): ')
        values = move.split(',')
        row, col = int(values[0]), int(values[1])
        return row, col

    def display_illegal_move_message(self, row, col):
        print('Illegal move. Try again.')

    def display_winner(self, player):
        print(f"Player {color_to_symbol[player.color]} won!")

    def show_draw(self):
        print('Game ended in a draw.')

    def display_board(self):
        print(self.game_board)
