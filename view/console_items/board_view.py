from abc import ABC, abstractmethod

class BoardView(ABC):
    """
    An abstract base class that defines a standard interface for displaying a game board. This class serves as a template 
    for creating various views (e.g., graphical user interface, text-based interface) that represent the game board in 
    different environments or frameworks.
    """    
    def __init__(self) -> None:
        """
        Initializes a new instance of a BoardView. This constructor might be used in subclasses to initialize components 
        necessary for displaying the board.
        """       
       pass

    @abstractmethod
    def display_board(self):
        """
        An abstract method that must be implemented by subclasses to handle the specifics of displaying the game board 
        in a particular format. This method should ensure that the board is rendered to the user based on the current 
        state of the game.
        """        
        pass