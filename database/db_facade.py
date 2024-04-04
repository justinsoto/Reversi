from model.game import Game
from view.console_items.console_game_view import ConsoleGameView
from controller.controller import GameController
from mysql.connector import connect, Error
from getpass import getpass
from database.db_management.user_manager import UserManager
from database.db_management.games_manager import GamesManager
from database.db_management.ratings_manager import RatingsManager
from database.db_management.user_manager_decorator import LoginDecorator

class database:
    def __init__(self):
        connection = connect(host='localhost', user='test', password='test123', database="reversi" )
        self.connection = connection
        self.ratings_manager = RatingsManager(connection)
        self.games_manager = GamesManager(connection)
        self.player1_id = None
        self.player2_id = None
        self.game_id = None
        self.login_manager = LoginDecorator(connection, UserManager(connection))

    def create_users(self):
        print("Player 1: \n")
        self.user_manager.create_user(input("Please Enter Your Username: "),getpass("Please Enter Your Password: "))
        self.player1_id = self.user_manager.get_current_user().get_user_id()
        print("Player 2: \n")
        self.user_manager.create_user(input("Please Enter Your Username: "),getpass("Please Enter Your Password: "))
        self.player2_id = self.user_manager.get_current_user().get_user_id()
        self.game_id = self.games_manager.create_game(self.player1_id, self.player2_id)

    def login_users(self):
        p = False
        while p == False:
            print("Player 1: ")
            p = self.login_manager.login(input("Please enter your username: "), getpass("Please enter your password: "))
            if p == False:
                print("Invalid Username/Password Combo. Please try again or create new user")
            else:
                self.player1_id = p
        q = False
        while q == False:
            print("Player 2: ")
            q = self.login_manager.login(input("Please enter your username: "), getpass("Please enter your password: "))
            if q == False:
                print("Invalid Username/Password Combo. Please try again or create new user")
            else:
                self.player2_id = q
        self.game_id = self.games_manager.create_game(self.player1_id, self.player2_id)

    def check_ratings_exist(self):
        if self.ratings_manager.get_rating(self.player1_id):
            pass
        else:
            self.ratings_manager.create_rating(self.player1_id, 0, 0, 0)

        if self.ratings_manager.get_rating(self.player2_id):
            pass
        else:
            self.ratings_manager.create_rating(self.player2_id, 0, 0, 0)

    def update_game_state(self, new_game_state):
        self.games_manager.update_game_state(self.game_id, new_game_state)

    def update_ratings_win(self, winner, loser, topScore):
        self.ratings_manager.update_top_score(winner, topScore)
        self.ratings_manager.update_wins(winner)
        self.ratings_manager.update_losses(loser)
        self.ratings_manager.update_elo_rating(winner, self.ratings_manager.get_elo_rating(loser), 1)
        self.ratings_manager.update_elo_rating(loser, self.ratings_manager.get_elo_rating(winner), -1)

    def update_ratings_draw(self):
        self.ratings_manager.update_elo_rating(self.player1_id, self.ratings_manager.get_elo_rating(self.player2_id), 0)
        self.ratings_manager.update_elo_rating(self.player2_id, self.ratings_manager.get_elo_rating(self.player2_id), 0)