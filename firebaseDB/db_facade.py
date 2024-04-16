import firebase_admin
from firebase_admin import credentials, firestore
from firebaseDB.db_management.user_manager import UserManager
from firebaseDB.db_management.games_manager import GamesManager
from firebaseDB.db_management.ratings_manager import RatingsManager

cred = credentials.Certificate(r"firebaseDB\softwareengineeringproje-b3db3-firebase-adminsdk-5k21y-3119caacb7.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

class database:
    def __init__(self):
        self.userManager = UserManager(db)
        self.ratingManager = RatingsManager(db)
        self.gameManager = GamesManager(db)

        self.loginPlayerID = ""
        self.OpponentPlayerID = ""
        self.gameID = ""

    def create_user(self, username, password):
        #use for register button
        self.loginPlayerID = self.userManager.create_user(username, password)

    def login_user(self, username, password):
        #use for login button
        self.loginPlayerID = self.userManager.login_user(username, password)

    def check_ratings_exist(self, user_id):
        #use after login and opponent user are confirmed
        self.ratingManager.create_rating(user_id)

    def update_game_state(self, game_id, new_game_state):
        #use to update game state in database after moves
        self.gameManager.update_game_state(game_id, new_game_state)

    def get_game_state(self, game_id):
        #use to pull game state from database between moves
        return self.gameManager.get_game_state(game_id)

    def create_game(self, gameState):
        #use to create a game with passed in game state from model when game config items are selected
        self.gameID = self.gameManager.create_game(self.loginPlayerID, self.OpponentPlayerID, gameState)

    def update_ratings_win(self, winner_id, loser_id, topScore):
        #use to update ratings for both players once a game is over and one player has won
        self.ratingManager.update_top_score(winner_id, topScore)
        self.ratingManager.update_wins(winner_id)
        self.ratingManager.update_losses(loser_id)
        self.ratingManager.update_elo_rating(winner_id, self.ratingManager.get_elo_rating(loser_id), 1)
        self.ratingManager.update_elo_rating(loser_id, self.ratingManager.get_elo_rating(winner_id), -1)

    def update_ratings_draw(self, player1_id, player2_id):
        #use to update ratings for both players once a game is over and it ends in a tie
        self.ratingManager.update_ties(player1_id)
        self.ratingManager.update_ties(player2_id)
        self.ratingManager.update_elo_rating(player1_id, self.ratingManager.get_elo_rating(player2_id), 0)
        self.ratingManager.update_elo_rating(player2_id, self.ratingManager.get_elo_rating(player1_id), 0)
