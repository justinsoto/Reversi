# app.py (Flask App to serve as backend)
from flask import Flask, jsonify
from flask_cors import CORS
from model.game import Game
from model.player import Player

app = Flask(__name__)
CORS(app)

game = Game(8)

@app.route('/')
def main_page():
    return "Main Page"

@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/score/<player>')
def get_score(player: Player):
    return game.get_player_score(player)

@app.route('/board-size')
def get_board_size():
    size = game.board.get_size()
    return jsonify({'size': size})

if __name__ == '__main__':
    app.run(debug=True)