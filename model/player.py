from model.player_color import PlayerColor

class Player:
    def __init__(self, color: PlayerColor) -> None:
        self.color = color

    def get_color(self) -> PlayerColor:
        return self.color