from abc import ABC, abstractmethod

class GameView(ABC):
    """
    An abstract base class that defines the standard interface for game views. This class provides the blueprint for 
    displaying game states, handling player interactions, and updating game information in various types of views, 
    such as graphical user interfaces or text-based consoles.
    """    
    def __init__(self) -> None:
        """
        Initializes the GameView instance. Concrete implementations may use this to set up necessary components or 
        state relevant to the specific type of view.
        """        
        pass

    @abstractmethod
    def display_current_player(self):
        """
        Abstract method to display the current player's turn in the game view.
        """        
        pass

    @abstractmethod
    def display_illegal_move_message(self, row, col):
        """
        Abstract method to display a message indicating that an attempted move at the specified coordinates is illegal.

        Parameters:
        row (int): The row index where the illegal move was attempted.
        col (int): The column index where the illegal move was attempted.
        """        
        pass

    @abstractmethod
    def display_winner(self):
        """
        Abstract method to display the winner of the game.
        """        
        pass

    @abstractmethod
    def display_draw_message(self):
        """
        Abstract method to display a message indicating that the game has ended in a draw.
        """        
        pass

    @abstractmethod
    def display_score(self, player):
        """
        Abstract method to display the current score for a specified player.

        Parameters:
        player: The player whose score is to be displayed. This could be an instance of a Player class or a similar object.
        """        
        pass

    @abstractmethod
    def display_legal_moves(self, player):
        """
        Abstract method to display all legal moves available to the specified player. If no player is specified,
        it should display all legal moves for the current player.

        Parameters:
        player (optional): The player for whom to display legal moves. If None, assumes the current player.
        """        
        pass

    @abstractmethod
    def display_legal_moves(self):
        """
        Abstract method to display all legal moves available currently in the game. This method should display legal moves 
        for the current player's turn without requiring specific player identification.
        """        
        pass

    @abstractmethod
    def display_final_scoreboard(self):
        """
        Abstract method to display the final scores of all players at the end of the game.
        """        
        pass

    @abstractmethod
    def get_move(self):
        """
        Abstract method to interactively retrieve a move from the player. This method is expected to return the
        move chosen by the player, which could be in various formats depending on the implementation.

        Returns:
        The move entered by the player, which might be a coordinate pair, a command string, etc.
        """        
        pass
