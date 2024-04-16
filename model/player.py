from model.player_color import PlayerColor

class Player:
    def __init__(self, color: PlayerColor, playerID) -> None:
        self.color = color
        self.id = playerID

    def get_color(self) -> PlayerColor:
        return self.color
