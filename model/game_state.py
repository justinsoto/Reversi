class GameState():
    '''Implemention of the Momento design pattern. Stores an instance of the model's current state.'''
    
    def __init__(self, current_player, scores, board) -> None:
        self.current_player = current_player
        self.scores = scores
        self.board = board
