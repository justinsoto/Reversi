from model.game import Game
from view.game_view import GameView
from model.player import Player
from model.player_color import color_to_symbol

class BoardView(GameView):
    def __init__(self, game: Game) -> None:
        super().__init__()
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

    def display_illegal_move_message(self):
        print('Illegal move. Try again.')

    def display_winner(self, winner: Player):
        print(f"Player {color_to_symbol[winner.get_color()]} won!")

    def display_draw_message(self):
        print('Game has ended in a draw.')

    def display_board(self):
        print(self)

    def display_score(self, player: Player):
         score = self.game.get_player_score(player)
         player_symbol = color_to_symbol[player.get_color()]
         print(f'Player {player_symbol} Score: {score} points.')

    def display_legal_moves(self):
        moves = self.game.find_legal_moves()

        if not moves:
            print("No legal moves available :(")
            self.game.swap_turns()
            return 
        
        print("Legal moves available:")
        for move in moves:
            row, col = move
            print(f'(row, col): {row}, {col}')

    # Displays all final scores after the game ends 
    def display_final_scorebaord(self):
        for player in self.game.get_all_players():
            self.display_score(player)
