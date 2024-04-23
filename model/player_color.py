"""
Defines the PlayerColor enumeration for representing different player colors and states on a game board, 
along with a dictionary to map these colors to specific display symbols.
"""

from enum import IntEnum

class PlayerColor(IntEnum):
    """
    An enumeration for representing the state of a cell in the game, either being empty, occupied by a black piece,
    or occupied by a white piece. These values are integral to the logic and rendering of the game state.
    """    
    Empty = 0 # Represents an empty cell on the game board.
    Black = 1 # Represents a cell occupied by a black piece.
    White = 2 # Represents a cell occupied by a white piece.

color_to_symbol = {
    PlayerColor.Empty: '_', # Symbol representing an empty space on the board.
    PlayerColor.Black: '●', # Symbol representing a black piece on the board.
    PlayerColor.White: '○'  # Symbol representing a white piece on the board.
}
