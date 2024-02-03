from model.game import Game
from view.board_view import BoardView
game = Game()
view = BoardView(game.board)
move = view.get_move()
row,col = move
game.make_move(row,col)
print(game)