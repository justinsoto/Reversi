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
    """
    Serves the main page of the application.

    Returns:
    str: A simple string indicating the user has reached the main page.
    """
    return "Main Page"

@app.route('/hello')
def hello():
    """
    A simple endpoint for testing that the service is operational.

    Returns:
    str: A greeting string 'Hello, World!'
    """    
    return 'Hello, World!'

# Returns the size of the board
@app.route('/board-size')
def get_board_size():
    """
    Retrieves the current size of the game board.

    Returns:
    JSON: A JSON object containing the size of the board.
    """    
    size = game.get_board_size()
    return jsonify({'size': size})

# Returns the player's current score
@app.route('/scores')
def get_scores():
    """
    Retrieves the current scores for both players in the game.

    Returns:
    tuple: A tuple containing the scores for player 1 and player 2.
    """
    p1 = game.get_player_score(game.player1)
    p2 = game.get_player_score(game.player2)
    return p1, p2

# Swaps player's turn, returns the new current player
@app.route('/pass-turn')
def pass_turn():
    """
    Passes the turn to the next player and returns the current player after the turn is passed.

    Returns:
    str: The string representation of the current player after passing the turn.
    """    
    controller.pass_turn()
    return get_current_player()

# Returns the player whose currently making a move
@app.route('/current-player')
def get_current_player():
    """
    Retrieves the current player of the game.

    Returns:
    str: The string representation of the current player.
    """    
    return controller.player_to_str(game.current_player)

@app.route('/board')
def get_board_state():
    """
    Retrieves the entire state of the game board.

    Returns:
    list: A nested list representing the state of each cell on the game board.
    """    
    size = game.get_board_size()
    board = [[controller.get_cell(row, col) for col in range(size)] for row in range(size)]
    # return jsonify({'board': board})
    return board

# Calls controller to execute a move
@app.route('/execute-move/<row>/<col>')
def execute_move(row, col):
    """
    Executes a move on the board at the specified row and column indices.

    Parameters:
    row (str): The row index where the move is to be made.
    col (str): The column index where the move is to be made.

    Returns:
    str: A message indicating that the move has been executed and which player made the move.
    """    
    row, col = int(row), int(col)
    current = game.get_current_player()
    print("database flag:", database_Flag)
    print(db.get_username_current_player(game.current_player.id))
    if database_Flag:
        if game.current_player.id == db.loginPlayerID:
            game.deserialize_game_state(db.get_game_state(db.gameID))
            controller.execute_move(row, col)
            print("updating database")
            db.update_game_state(db.gameID, game.serialize_game_state())
        game.deserialize_game_state(db.get_game_state(db.gameID))
    else:
        controller.execute_move(row, col)
    return f'Move Executed {row} {col} by {controller.player_to_str(current)}'

# Triggers the AI to execute a move
@app.route('/trigger-ai')
def trigger_AI():
    """
    Triggers the AI to execute a move if enabled.

    Returns:
    str: A message indicating the result of the AI's action or stating that the AI is disabled.
    """    
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
    """
    Checks if the AI feature is enabled in the game.

    Returns:
    bool: True if AI is enabled, False otherwise.
    """    
    return controller.aiEnabled

# Toggles AI Status
@app.route('/toggle-ai')
def toggle_ai_status():
    """
    Toggles the AI feature on or off and resets the game to its initial state.

    Returns:
    str: A message indicating the AI status has been updated.
    """    
    controller.toggle_ai_status()
    controller.reset_game()
    return 'AI Status Updated'

# Restarts the game
@app.route('/reset')
def reset_game():
    """
    Resets the game to its initial state.

    Returns:
    str: A message indicating the game has been reset.
    """    
    controller.reset_game()
    return "Game Reset"

@app.route('/default-settings')
def default_settings():
    """
    Resets the game to default settings, disabling AI and any database flags.

    Returns:
    str: A simple OK message indicating successful resetting to default settings.
    """    
    global database_Flag
    if controller.aiEnabled:
        controller.toggle_ai_status()
    database_Flag = False
    return 'OK'

@app.route('/message')
def get_message():
    """
    Generates a message based on the current game state, including game over conditions.

    Returns:
    str: A message reflecting the current state or outcome of the game.
    """    
    if game.game_over():
        if controller.get_winner():
            winner = controller.player_to_str(controller.get_winner())
            winner_id = controller.get_winner().id
            loser_id = controller.get_loser().id
            db.update_ratings_win(winner_id, loser_id, game.get_player_score(winner))
            return f'{winner} wins!' if winner else "Draw."
        else:
            db.update_ratings_draw(game.player1.id, game.player2.id)
        db.delete_game(db.gameID)
    if controller.is_AI_making_move():
        return "AI is making a move..."

    return f"{get_current_player()}'s turn"

# Returns the current state of the game
@app.route('/game-state')
def get_game_state():
    """
    Retrieves the complete current state of the game, including player scores, the current player, and board state.

    Returns:
    JSON: A JSON object containing comprehensive game state information.
    """    
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
    """
    Attempts to log in a user with the provided username and password.

    Parameters:
    username (str): The username of the user attempting to log in.
    password (str): The password of the user attempting to log in.

    Returns:
    JSON: A JSON object indicating the result of the login attempt and any associated messages.
    """    
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
    """
    Registers a new user with the provided username and password.

    Parameters:
    username (str): The username for the new user.
    password (str): The password for the new user.

    Returns:
    JSON: A JSON object indicating the result of the registration attempt and any associated messages.
    """    
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
    """
    Retrieves a list of all registered users.

    Returns:
    JSON: A JSON object containing a list of registered users.
    """    
    users = db.list_current_users()
    return jsonify({'users': users})

# Starts a game with one human player and the AI
@app.route('/play-ai')
def playAI():
    """
    Starts a game against the AI.

    Returns:
    None
    """    
    if not controller.aiEnabled:
        controller.toggle_ai_status()
    return

# Starts a game with two human players
@app.route('/play-user/<username>')
def playUser(username):
    """
    Initiates a game against another human player identified by username.

    Parameters:
    username (str): The username of the opponent player.

    Returns:
    str: A simple OK message indicating that the game setup is complete.
    """    
    global database_Flag
    database_Flag = True
    if controller.aiEnabled == True:
        controller.aiEnabled = False
    db.set_opponent(username)

    if not db.check_rating_exists(db.loginPlayerID):
        db.create_rating(db.loginPlayerID)
    if not db.check_rating_exists(db.OpponentPlayerID):
        db.create_rating(db.OpponentPlayerID)

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
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)