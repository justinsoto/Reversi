from model.game import Game
from view.board_view import BoardView
from controller.controller import GameController
game = Game(4)
view = BoardView(game)
<<<<<<< Updated upstream
controller = GameController (game,view)
controller.start_game()
=======
print(view)
while not game.game_over():
    view.display_current_player()
    game.print_score()
    game.find_legal_moves()
    row, col = view.get_move()
    game.make_move(row, col)
    print(view)

game.print_winner()
>>>>>>> Stashed changes
