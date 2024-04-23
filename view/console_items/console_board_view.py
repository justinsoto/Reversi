from model.board import Board
from model.player_color import color_to_symbol

class ConsoleBoardView():
    """
    Provides a console-based view of a game board, allowing for text representation of the board state. This class is 
    designed to display the board in a simple text format, using predefined symbols to represent the state of each cell.
    """    
    def __init__(self, board: Board):
        """
        Initializes the ConsoleBoardView with a specific board.

        Parameters:
        board (Board): The game board that this view will represent.
        """        
        self.board = board

    # Creates text-based version of the game
    def __str__(self) -> str:
        """
        Generates a string representation of the board state, suitable for printing to the console. This method 
        loops through each row and cell of the board, converting player colors to symbols defined in the 
        'color_to_symbol' dictionary, and formats them into a string that represents the board.

        Returns:
        str: A text representation of the board, where each row is on a new line and cells are separated by spaces.
        """        
        game_string = ''
        for row in self.board.get_board():
            for piece in row:
                game_string += ' ' + color_to_symbol[piece] + ' '
            game_string += '\n'
        return game_string
