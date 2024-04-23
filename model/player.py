from model.player_color import PlayerColor

class Player:
    """
    Represents a player in the game, holding information about the player's color and unique identifier.
    """    
    def __init__(self, color: PlayerColor, playerID) -> None:
        """
        Initializes a new instance of the Player class with a specified color and player ID.

        Parameters:
        color (PlayerColor): The color assigned to the player, which is an enumeration value of PlayerColor.
        playerID (str): The unique identifier for the player.
        """        
        self.color = color
        self.id = playerID

    def get_color(self) -> PlayerColor:
        """
        Retrieves the color of the player.

        Returns:
        PlayerColor: The color enumeration value representing the player's color.
        """        
        return self.color