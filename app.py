from flask import Flask, jsonify
from flask_cors import CORS
from model.game import Game
from model.player import Player
from controller.gui_controller import GUIController
# from mysql.connector import connect, Error
# from getpass import getpass
# from model.db_management.user_manager import UserManager
# from model.db_management.games_manager import GamesManager
# from model.db_management.ratings_manager import RatingsManager
# from model.db_management.leaderboard_manager import LeaderboardManager

app = Flask(__name__)
CORS(app)

game = Game(8)
controller = GUIController(game)
# connection = connect(host ='localhost', user = input('Enter Username: '), password = getpass('Enter Pasword: '), database="Othello" )
# user_manager = UserManager(connection)
# ratings_manager = RatingsManager(connection)
# games_manager = GamesManager(connection)
# leaderboard_manager = LeaderboardManager(connection)

# user_manager.create_user("User1","test")
# user_id = user_manager.get_current_user().get_user_id()

# user_manager.create_user("User2","test1")
# user_id2 = user_manager.get_current_user().get_user_id()

# ratings_manager.create_rating(0, 0, 0)
# ratings_manager.create_rating(0, 0, 0)

# games_manager.create_game(user_id, user_id2)
# game_id = games_manager.get_current_game().get_game_id()

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
    return scores

# Swaps player's turn, returns the new current player
@app.route('/pass-turn')
def pass_turn():
    controller.pass_turn()
    return get_current_player()

# Returns the player whose currently making a move
@app.route('/current-player')
def get_current_player():
    return controller.player_to_str(game.current_player)

@app.route('/board')
def get_board_state():
    size = game.get_board_size()
    board = [[controller.get_cell(row, col) for col in range(size)] for row in range(size)]
    # db.update_game_state(game.serialize_game_state())
    return jsonify({'board': board})

# Calls controller to execute a move
@app.route('/execute-move/<row>/<col>')
def execute_move(row, col):
    row, col = int(row), int(col)
    controller.execute_move(row, col)
    return

# Triggers the AI to execute a move
@app.route('/trigger-ai')
def trigger_AI():
    controller.execute_AI_move()
    return

# Returns True if the AI feature is enabled
@app.route('/ai-status')
def get_ai_status():
    return controller.aiEnabled

@app.route('/toggle-ai')
def toggle_ai_status():
    controller.toggle_ai_status()
    controller.reset_game()
    return

# Restarts the game
@app.route('/reset')
def reset_game():
    controller.reset_game()
    return

@app.route('/message')
def get_message():
    # if game.game_over():
    #     winner = game.declare_winner()
    #     if winner == game.player1:
    #         db.update_ratings_win(db.player1_id, db.player2_id, game.get_player_score(winner))
    #     elif winner == game.player2 and not ai_flag:
    #         db.update_ratings_win(db.player2_id, db.player1_id, game.get_player_score(winner))
    #     else:
    #         db.update_ratings_draw()
    # if game.game_over():
    #     winner = game.declare_winner()
    #     u1_elo = ratings_manager.get_elo_rating(user_id)
    #     u2_elo = ratings_manager.get_elo_rating(user_id2)
    #     if winner == game.player1:
    #         ratings_manager.update_top_score(user_id, game.get_player_score(game.player1))
    #         ratings_manager.update_wins(user_id)
    #         ratings_manager.update_losses(user_id2)
    #         ratings_manager.update_elo_rating(user_id, u2_elo, 1)
    #         ratings_manager.update_elo_rating(user_id2, u1_elo, -1)
    #     elif winner == game.player2 and not ai_flag:
    #         ratings_manager.update_top_score(user_id2, game.get_player_score(game.player2))
    #         ratings_manager.update_wins(user_id2)
    #         ratings_manager.update_losses(user_id)
    #         ratings_manager.update_elo_rating(user_id2, u1_elo, 1)
    #         ratings_manager.update_elo_rating(user_id, u2_elo, -1)
    #     elif winner == None:
    #         #update draws for both players once function is available
    #         ratings_manager.update_elo_rating(user_id2, u1_elo, 0)
    #         ratings_manager.update_elo_rating(user_id, u2_elo, 0)
    #     return f"{player_to_string[winner]} won!"

    if game.game_over():
        winner = controller.player_to_str(controller.get_winner())
        return f'{winner} wins!' if winner else "Draw." 

    return f"{get_current_player()}'s turn"

# Returns the current state of the game 
@app.route('/game-state')
def get_game_state():
    p1, p2 = get_scores()
    return jsonify({
        'currentPlayer': controller.player_to_str(game.get_current_player()),
        'scores': {"player1": game.get_player_score(game.player1), "player2": game.get_player_score(game.player2)},
        'message': get_message(),
        'aiStatus': get_ai_status(),
        # 'board': get_board_state()
    })

if __name__ == '__main__':
    app.run(debug=True)
