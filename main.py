from model.board import Board
from view.text_view import TextView

board = Board(8)
game = TextView(board.get_board())
print(game.__str__())
