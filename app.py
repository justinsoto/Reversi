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
    size = game.board.get_size()
    return jsonify({'size': size})

# Returns the player's current score 
@app.route('/scores')
def get_score():
    scores = [game.get_player_score(player) for player in game.get_all_players()]
    return jsonify({'player1': scores[0],
                    'player2': scores[1]})

@app.route('/board', methods=['GET'])
def get_board_state():
    # assuming our Game class has a method to get the board's current state 
    # and that it returns a 2D list (or similar) that represents the board
    board_state = game.board.get_state()
    return jsonify(board_state)

@app.route('/pass-turn')
def pass_turn():

@app.route('/messages')
def messages():

if __name__ == '__main__':
    app.run(debug=True)