# app.py (Flask App to serve as backend)
from flask import Flask, jsonify
from model.game import Game
from model.player import Player

app = Flask(__name__)
game = Game(10)

@app.route('/')
def main_page():
    return "Main Page"

@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/score/<player>')
def get_score(player: Player):
    return game.get_player_score(player)

@app.route('/game-size')
def get_game_size():
    size = game.board.get_size()
    return jsonify({'size': size})

if __name__ == '__main__':
    app.run()