# app.py (Flask App to serve as backend)
from flask import Flask, jsonify
from flask_cors import CORS
from model.game import Game
from model.player import Player
from model.player_color import PlayerColor

app = Flask(__name__)
CORS(app)

game = Game(8)

@app.route('/')
def main_page():
    return "Main Page"

@app.route('/hello')
def hello():
    return 'Hello, World!'

# Returns the size of the board 
@app.route('/board-size')
def get_board_size():
    size = game.get_board_size()
    return jsonify({'size': size})

# Returns the player's current score 
@app.route('/scores')
def get_scores():
    scores = [game.get_player_score(player) for player in game.get_all_players()]
    return jsonify({'player1': scores[0],
                    'player2': scores[1]})

<<<<<<< Updated upstream
# Return the current state of the board
@app.route('/board', methods=['GET'])
def get_board_state():
    # assuming our Game class has a method to get the board's current state 
    # and that it returns a 2D list (or similar) that represents the board
    board_state = game.board.get_state()
    return jsonify(board_state)

@app.route('/pass-turn')
def pass_turn():
    # Simple toggle between player1 and player2 as the current player
    if game.current_player == game.player1:
        game.current_player = game.player2
    else:
        game.current_player = game.player1
    
    # Assuming we have a method to return the current player's identifier (e.g., name, color, or ID)
    # If not, we might simply return a message indicating the turn has been passed
    # We just need to make sure both our game and player class support this logic    
    return jsonify({"currentPlayer": game.current_player.get_identifier()})

@app.route('/messages')
def messages():
=======
# @app.route('/board')
# def get_board():
#     board = game.board.get_board()
#     for row in range(len(board)):
#         for col in range(len(board[row])):
#             cell = board[row][col]
#             if cell == PlayerColor.Black:
#                 cell = 'black'
#             if cell == PlayerColor.White:
#                 cell = 'white'
#             if cell == PlayerColor.Empty:
#                 cell = 'empty'
#     return jsonify({'board': board})


>>>>>>> Stashed changes

if __name__ == '__main__':
    app.run(debug=True)