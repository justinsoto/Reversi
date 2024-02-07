from model.game import Game
from view.board_view import BoardView
game = Game(4)

view = BoardView(game)
print(view)
while not game.game_over():
    view.show_curr_player()
    game.print_score()
    game.print_legal_moves()
    row, col = view.get_move()
    game.make_move(row, col)
    print(view)

game.print_winner()