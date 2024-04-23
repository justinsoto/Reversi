from model.game import Game
from model.player import Player
from model.player_color import color_to_symbol
from view.console_items.console_board_view import ConsoleBoardView

class ConsoleGameView():
    """
    A console-based view for displaying the state of the game, including the board, current player, scores, and 
    available legal moves. This view updates the user via standard output (console) and handles user inputs for moves.
    """    
    def __init__(self, game: Game) -> None:
        """
        Initializes the console view with a reference to the game instance.

        Parameters:
        game (Game): The game instance this view will display.
        """        
        self.game = game
        self.board_view = ConsoleBoardView(game.board)

    def display_board(self):
        """
        Updates and displays the game board. This method is typically called after the game state has changed, such as
        after a move has been made or the game has been loaded from a database.
        """        
        #necessary to update board view if game is pulled from database
        self.board = self.game.board
        self.board_view = ConsoleBoardView(self.board)
        print(self.board_view)

    def display_current_player(self):
        """
        Displays which player's turn it is.
        """       
       curr_player = self.game.get_current_player_color()
       print(f"It's {color_to_symbol[curr_player]}'s turn. ")

    def display_illegal_move_message(self):
        """
        Displays a message to the console indicating that an attempted move was illegal.
        """        
        print('Illegal move. Try again.')

    def display_winner(self, winner: Player):
        """
        Displays the winner of the game.

        Parameters:
        winner (Player): The player who has won the game.
        """        
        print(f"Player {color_to_symbol[winner.get_color()]} won!")

    def display_draw_message(self):
        """
        Displays a message indicating that the game has ended in a draw.
        """        
        print('Game has ended in a draw.')

    def display_score(self, player: Player):
        """
        Displays the score for a given player.

        Parameters:
        player (Player): The player whose score is to be displayed.
        """         
         score = self.game.get_player_score(player)
         player_symbol = color_to_symbol[player.get_color()]
         print(f'Player {player_symbol} Score: {score} points.')

    def display_legal_moves(self):
        """
        Displays all legal moves available to the current player. If no moves are available, it indicates so and swaps
        turns automatically.
        """        
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
        """
        Displays the final scores for all players after the game has concluded.
        """        
        for player in self.game.get_all_players():
            self.display_score(player)

    def get_move(self):
        """
        Prompts the user to enter their move via the console. Allows for a 'pass' option by entering 'p'.

        Returns:
        tuple/int/str: Returns the move as a tuple (row, col), 'p' for passing, or continues prompting if input is invalid.
        """        
        move = input('Enter your move (row, col): ')

        # Pass turn key
        if move == "p":
            return move

        values = move.split(',')
        row, col = int(values[0]), int(values[1])
        return row, col
