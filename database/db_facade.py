from mysql.connector import connect
from getpass import getpass
from database.user_manager_proxy import UserManagerProxy
from database.db_management.games_manager import GamesManager
from database.db_management.ratings_manager import RatingsManager

class database:
    def __init__(self):
        connection = connect(host='localhost', user='test', password='test123', database="reversi" )
        self.connection = connection
        self.ratings_manager = RatingsManager(connection)
        self.games_manager = GamesManager(connection)
        self.user_manager_proxy = UserManagerProxy(connection)
        self.player1_id = None
        self.player2_id = None
        self.game_id = None

    def create_users(self):
        print("Player 1: \n")
        self.user_manager_proxy.create_user(input("Please Enter Your Username: "),getpass("Please Enter Your Password: "))
        self.player1_id = self.user_manager_proxy.get_current_user().get_user_id()
        print("Player 2: \n")
        self.user_manager_proxy.create_user(input("Please Enter Your Username: "),getpass("Please Enter Your Password: "))
        self.player2_id = self.user_manager_proxy.get_current_user().get_user_id()
        self.game_id = self.games_manager.create_game(self.player1_id, self.player2_id)

    def login_users(self, username, password, player):
        test = self.user_manager_proxy.login(username, password)
        if test == False:
            return test
        else:
            if player == 1:
                self.player1_id = test
            else:
                self.player2_id == test
            return True

    #add function to create a game using passed in userIDs

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
