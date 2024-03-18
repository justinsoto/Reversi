# app.py (Flask App to serve as backend)
from flask import Flask, jsonify
from flask_cors import CORS
from model.game import Game
from model.player import Player
from controller.gui_controller import GUIController
from mysql.connector import connect, Error
from getpass import getpass
from model.db_management.user_manager import UserManager
from model.db_management.games_manager import GamesManager
from model.db_management.ratings_manager import RatingsManager
from model.db_management.leaderboard_manager import LeaderboardManager

app = Flask(__name__)
CORS(app)

game = Game(8)
controller = GUIController(game)
connection = connect(host ='localhost', user = input('Enter Username: '), password = getpass('Enter Pasword: '), database="Othello" )
user_manager = UserManager(connection)
ratings_manager = RatingsManager(connection)
games_manager = GamesManager(connection)
leaderboard_manager = LeaderboardManager(connection)

players = game.get_all_players()
player_to_string = {
    players[0]: "Player 1",
    players[1]: "Player 2"
}

user_manager.create_user("User1","test")
user_id = user_manager.get_current_user().get_user_id()

user_manager.create_user("User2","test1")
user_id2 = user_manager.get_current_user().get_user_id()

ratings_manager.create_rating(0, 0, 0)
ratings_manager.create_rating(0, 0, 0)

games_manager.create_game(user_id, user_id2)
game_id = games_manager.get_current_game().get_game_id()

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
    games_manager.update_game_state(game_id, game.serialize_game_state())
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

@app.route('/message')
def get_message():
    if game.game_over():
        winner = game.declare_winner()
        u1_elo = ratings_manager.get_elo_rating(user_id)
        u2_elo = ratings_manager.get_elo_rating(user_id2)
        if winner == game.player1:
            ratings_manager.update_top_score(user_id, game.get_player_score(game.player1))
            ratings_manager.update_wins(user_id)
            ratings_manager.update_losses(user_id2)
            ratings_manager.update_elo_rating(user_id, u2_elo, 1)
            ratings_manager.update_elo_rating(user_id2, u1_elo, -1)
        elif winner == game.player2 and not ai_flag:
            ratings_manager.update_top_score(user_id2, game.get_player_score(game.player2))
            ratings_manager.update_wins(user_id2)
            ratings_manager.update_losses(user_id)
            ratings_manager.update_elo_rating(user_id2, u1_elo, 1)
            ratings_manager.update_elo_rating(user_id, u2_elo, -1)
        elif winner == None:
            #update draws for both players once function is available
            ratings_manager.update_elo_rating(user_id2, u1_elo, 0)
            ratings_manager.update_elo_rating(user_id, u2_elo, 0)
        return f"{player_to_string[winner]} won!"

    current_player = game.get_current_player()
    return f"{player_to_string[current_player]}'s turn"

if __name__ == '__main__':
    app.run(debug=True)
