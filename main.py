'''from model.game import Game
from view.console_game_view import ConsoleGameView
from controller.controller import GameController

game = Game(16)
view = ConsoleGameView(game)
controller = GameController(game,view)
controller.start_game()'''

from model.game import Game
from view.console_game_view import ConsoleGameView
from controller.controller import GameController
from mysql.connector import connect, Error
from getpass import getpass
from model.db_management.user_manager import UserManager
from model.db_management.games_manager import GamesManager
from model.db_management.leaderboard_manager import LeaderboardManager

    
try:
    connection = connect(
    host ='localhost',
    user = input('Enter Username: '),
    password = getpass('Enter Pasword: '),
    database="Othello" 
    )
    user_manager = UserManager(connection)
    games_manager = GamesManager(connection)
    leaderboard_manager = LeaderboardManager(connection)
  
    #can probaly pass these managers or the connection itself
    game = Game(8)
    view = ConsoleGameView(game)
    
    view.display_board()
    game.deserialize_game_state(games_manager.get_game_state(1))
    print("I PULLED THIS GAME FROM THE DATABSE -- NO MOVES MADE")
    view.display_board()
    

    



except Error as err:
    print("Error:", err)

finally:
        connection.close()
