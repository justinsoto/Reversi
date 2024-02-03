from model.game import Game
from view.board_view import BoardView
game = Game()

view = BoardView(game.board)
for i in range(5):
    move = view.get_move()
    row,col = move
    game.make_move(row,col)
    print(game)
    game.has_legal_move()
