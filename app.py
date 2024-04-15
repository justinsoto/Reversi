from flask import Flask, jsonify
from flask_cors import CORS
from model.game import Game
from controller.gui_controller import GUIController
from time import sleep

app = Flask(__name__)
CORS(app)

game = Game(8)
controller = GUIController(game)

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

if __name__ == '__main__':
    app.run(debug=True)
