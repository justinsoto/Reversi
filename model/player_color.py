from enum import IntEnum

class PlayerColor(IntEnum):
    Empty = 0
    Black = 1
    White = 2

color_to_symbol = {
    PlayerColor.Empty: '_',
    PlayerColor.Black: '@',
    PlayerColor.White: 'O'
}