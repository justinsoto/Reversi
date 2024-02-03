from view.text_view import TextView
from model.game import Game

game = Game()
print(game)
game.make_move(2, 4)
print(game)
game.has_legal_move()
game.make_move(2, 5)
print(game)
