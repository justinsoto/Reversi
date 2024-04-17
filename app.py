from flask import Flask, jsonify, request
from flask_cors import CORS
from model.game import Game
from controller.gui_controller import GUIController
from firebaseDB.db_facade import database
from time import sleep

app = Flask(__name__)
CORS(app)

game = Game(8, "", "")
controller = GUIController(game)

db = database()

ai_Flag = False
database_Flag = False

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
    print("database flag:", database_Flag)
    if database_Flag:
        if game.current_player.id == db.loginPlayerID:
            print("pulling from database")
            game.deserialize_game_state(db.get_game_state(db.gameID))
            controller.execute_move(row, col)
            print("updating database")
            db.update_game_state(db.gameID, game.serialize_game_state())
    else:
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

@app.route('/default-settings')
def default_settings():
    global ai_Flag
    global database_Flag

    database_Flag = False

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

# Returns a list of all registered users
@app.route('/users')
def get_users():
    users = db.list_current_users()
    return jsonify({'users': users})

# Starts a game with one human player and the AI
@app.route('/play-ai')
def playAI():
    if not controller.aiEnabled:
        controller.toggle_ai_status()
    return

# Starts a game with two human players
@app.route('/play-user/<username>')
def playUser(username):
    global database_Flag
    database_Flag = True
    if controller.aiEnabled == True:
        controller.aiEnabled = False
    db.set_opponent(username)
    p = db.check_game_exists(db.loginPlayerID, db.OpponentPlayerID)
    q = db.check_game_exists(db.OpponentPlayerID, db.loginPlayerID)
    if p:
        print("loading game 1")
        game_state = db.get_game_state(p)
        game.deserialize_game_state(game_state)
        db.gameID = p
        game.player1.id = db.loginPlayerID
        game.player2.id = db.OpponentPlayerID
    elif q:
        print("loading game 2")
        game_state = db.get_game_state(q)
        db.gameID = q
        game.deserialize_game_state(game_state)
        game.player2.id = db.loginPlayerID
        game.player1.id = db.OpponentPlayerID
    else:
        print("creating game")
        db.create_game(game.serialize_game_state())
        game.player1.id = db.loginPlayerID
        game.player2.id = db.OpponentPlayerID

    print("player1ID: ", game.player1.id)
    print("player2ID: ", game.player2.id)
    print("currentPlayerID: ", game.current_player.id)
    print(database_Flag)
    return

if __name__ == '__main__':
    app.run(debug=True)

#TODO:
# Edit make move function in the server to check current player's user ID with login_userID stored in database manager to determine if player can make a move or not
# move play ai button to opponent selection page
