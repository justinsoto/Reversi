from model.game import Game
from view.board_view import BoardView
game = Game()

view = BoardView(game)
print(view)
while True:
    view.show_curr_player()
    game.print_legal_moves()
    row, col = view.get_move()
    game.make_move(row, col)
    print(view)

