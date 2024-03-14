# app.py (Flask App to serve as backend)
from flask import Flask, jsonify
from flask_cors import CORS
from model.game import Game
from model.player import Player
from model.player_color import PlayerColor

app = Flask(__name__)
CORS(app)

game = Game(8)

players = game.get_all_players()
player_to_string = {
    players[0]: "Player 1",
    players[1]: "Player 2"
}


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

# Swaps player's turn 
@app.route('/pass-turn')
def pass_turn():
    game.swap_turns()
    return

# Returns the player whose currently making a move
@app.route('/current-player')
def get_current_player():
    return jsonify(player_to_string[game.get_current_player()])
    
    # Assuming we have a method to return the current player's identifier (e.g., name, color, or ID)
    # If not, we might simply return a message indicating the turn has been passed
    # We just need to make sure both our game and player class support this logic    
    #return jsonify({"currentPlayer": game.current_player.get_identifier()})

@app.route('/messages')
def messages():
    pass

if __name__ == '__main__':
    app.run(debug=True)