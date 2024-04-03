from flask import Flask, jsonify
from flask_cors import CORS
from model.game import Game
from model.player import Player
from controller.gui_controller import GUIController
from mysql.connector import connect, Error
from getpass import getpass
from database.db_facade import database

app = Flask(__name__)
CORS(app)

game = Game(8)
controller = GUIController(game)

players = game.get_all_players()
player_to_string = {
    players[0]: "Player 1",
    players[1]: "Player 2"
}

db = database()

createUserFlag = input("Do you need to create a new user (1) or log in (2)?")
if createUserFlag == 1:
    db.create_users()
elif createUserFlag == 2:
    db.login_users()

db.check_ratings_exist()

ai_flag = False

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
    db.update_game_state(game.serialize_game_state())
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

# Triggers the AI to execute a move
@app.route('/trigger-AI')
def trigger_AI():
    controller.execute_AI_move()
    return

# Returns True if the AI feature is enabled
@app.route('/AI-status')
def AI_status():
    return jsonify({'AI': controller.aiEnabled})

@app.route('/toggle-AI')
def toggle_AI():
    controller.toggle_AI()
    return

# Restarts the game
@app.route('/reset')
def reset_game():
    controller.reset_game()
    return

@app.route('/message')
def get_message():
    if game.game_over():
        winner = game.declare_winner()
        if winner == game.player1:
            db.update_ratings_win(db.player1_id, db.player2_id, game.get_player_score(winner))
        elif winner == game.player2 and not ai_flag:
            db.update_ratings_win(db.player2_id, db.player1_id, game.get_player_score(winner))
        else:
            db.update_ratings_draw()
    return f"{get_current_player()}'s turn"

if __name__ == '__main__':
    app.run(debug=True)
