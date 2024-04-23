class GameState():

    def __init__(self, current_player, scores, board) -> None:
        """
        Initializes a new GameState object with details about the current state of the game. This class is intended 
        to encapsulate the entire state of a game at a given point, including the current player, scores, and the 
        game board configuration.

        Parameters:
        current_player (Player): The player whose turn it is to move.
        scores (dict): A dictionary containing the scores of the players. Keys are player identifiers and values 
                       are their corresponding scores.
        board (list): A 2D list representing the current configuration of the game board, where each sublist 
                      represents a row and each item in the sublist represents a cell on the board.
        """        
        self.current_player = current_player
        self.scores = scores
        self.board = board
