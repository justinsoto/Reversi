# app.py (Flask App to serve as backend)
from flask import Flask, jsonify
from flask_cors import CORS
from model.game import Game
from model.player import Player
from controller.gui_controller import GUIController

app = Flask(__name__)
CORS(app)

game = Game(8)
controller = GUIController(game)

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
    controller.pass_turn()
    return

# Returns the player whose currently making a move
@app.route('/current-player')
def get_current_player():
    return player_to_string[game.get_current_player()]

@app.route('/board')
def get_board_state():
    size = game.get_board_size()
    board = [[get_cell_state(row, col) for col in range(size)] for row in range(size)]
    return jsonify({'board': board})

# Returns the state of the cell (empty, taken, legal)
@app.route('/cell-state/<row>/<col>')
def get_cell_state(row, col):
    row, col = int(row), int(col)

    legal_moves = game.find_legal_moves()
    if [row, col] in legal_moves:
        return "Legal"
    
    if not game.board.is_cell_empty(row, col):
        player = game.get_player_at_cell(row, col)
        return player_to_string[player]
    
    return "Empty"

# Calls controller to execute a move
@app.route('/execute-move/<row>/<col>')
def execute_move(row, col):
    row, col = int(row), int(col)
    controller.execute_move(row, col)
    return

# Restarts the game
@app.route('/reset')
def reset_game():
    controller.reset_game()
    return

@app.route('/messages')
def messages():
    pass

if __name__ == '__main__':
    app.run(debug=True)