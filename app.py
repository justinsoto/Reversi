from flask import Flask, jsonify, request
from flask_cors import CORS
from model.game import Game
from controller.gui_controller import GUIController
from firebaseDB.db_facade import database
from time import sleep

app = Flask(__name__)
CORS(app)

game = Game(8, "test", "test")
controller = GUIController(game)

db = database()

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
    p1 = game.get_player_score(game.player1)
    p2 = game.get_player_score(game.player2)
    return p1, p2

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
    # return jsonify({'board': board})
    return board

# Calls controller to execute a move
@app.route('/execute-move/<row>/<col>')
def execute_move(row, col):
    row, col = int(row), int(col)
    current = game.get_current_player()
    controller.execute_move(row, col)
    return f'Move Executed {row} {col} by {controller.player_to_str(current)}'

# Triggers the AI to execute a move
@app.route('/trigger-ai')
def trigger_AI():
    row, col = controller.get_AI_move()

    if row == -1 or col == -1:
        return f"AI Disabled {controller.player_to_str(game.current_player)}'s turn"

    current = game.get_current_player()
    sleep(1)
    controller.execute_move(row, col)
    return f"AI Move Executed {row} {col} by {controller.player_to_str(current)}"

# Returns True if the AI feature is enabled
@app.route('/ai-status')
def get_ai_status():
    return controller.aiEnabled

# Toggles AI Status
@app.route('/toggle-ai')
def toggle_ai_status():
    controller.toggle_ai_status()
    controller.reset_game()
    return 'AI Status Updated'

# Restarts the game
@app.route('/reset')
def reset_game():
    controller.reset_game()
    return "Game Reset"

@app.route('/message')
def get_message():
    if game.game_over():
        winner = controller.player_to_str(controller.get_winner())
        return f'{winner} wins!' if winner else "Draw."

    if controller.is_AI_making_move():
        return "AI is making a move..."

    return f"{get_current_player()}'s turn"

# Returns the current state of the game
@app.route('/game-state')
def get_game_state():
    p1, p2 = get_scores()
    return jsonify({
        'currentPlayer': controller.player_to_str(game.get_current_player()),
        'scores': {"player1": p1, "player2": p2},
        'message': get_message(),
        'aiStatus': get_ai_status(),
        'board': get_board_state()
    })

# Logs in user based on the entered username and password
@app.route('/login/<username>/<password>')
def login(username, password):
    loginResult = db.login_user(username, password)
    user_message = ''
    if loginResult:
        user_message = "Login Successful"
    else:
        user_message = "Login Unsuccessful"
    
    print(user_message)
    print(loginResult)
    return jsonify({'auth': loginResult, 'message': user_message})
#getting a TypeError when I try to return boolean for these functions so i just used strings for now

# Registers user in the database based on the entered username and password
@app.route('/register/<username>/<password>')
def register(username, password):
    registerResult = db.create_user(username,password)
    user_message = ''
    if registerResult:
        user_message = "Registration Successful"
    else:
        user_message = "User already exists"
    
    print(user_message)
    print(registerResult)
    return jsonify({'regAuth': registerResult, 'message': user_message})

@app.route('/users')
def get_users():
    users = db.list_current_users()
    return jsonify({'users': users})

if __name__ == '__main__':
    app.run(debug=True)

#TODO:
#add login and registration functions.
# Login use login users function to check if the passed username and password are in the database and if they are return verified authentication method, and if not return error message
# Registration function should check if the user already exists, and if it doesn't create the new user
# add opponent selection page that returns the opponent's userID or guest. If guest is selected, don't create a game in the database, otherwise check if a game exists, and if it does load the game, otherwise create a game
# Once game config page is added, add function that creates a model based off of passed in parameters and then creates the game in the database
# Edit make move function in the server to check current player's user ID with login_userID stored in database manager to determine if player can make a move or not
# move play ai button to opponent selection page
