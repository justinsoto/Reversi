from model.game import Game
from view.board_view import BoardView
game = Game()

view = BoardView(game.board)
print(game)
for i in range(5):
    game.print_legal_moves()
    row, col = view.get_move()
    game.make_move(row,col)
    print(game)
    
