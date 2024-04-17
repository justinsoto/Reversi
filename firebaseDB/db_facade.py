import os
import firebase_admin
from firebase_admin import credentials, firestore
from firebaseDB.db_management.user_manager import UserManager
from firebaseDB.db_management.games_manager import GamesManager
from firebaseDB.db_management.ratings_manager import RatingsManager

# Construct the file path using os.path.join
cred_path = os.path.join("firebaseDB", "softwareengineeringproje-b3db3-firebase-adminsdk-5k21y-3119caacb7.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

class database:
    def __init__(self):
        """
        Initialize the database class with instances of UserManager, RatingsManager, and GamesManager.
        It also initializes empty ID attributes for player login, opponent player, and game.
        """
        self.userManager = UserManager(db)
        self.ratingManager = RatingsManager(db)
        self.gameManager = GamesManager(db)

        self.loginPlayerID = ""
        self.OpponentPlayerID = ""
        self.gameID = ""

    def create_user(self, username, password):
        #use for register button
        """
        Registers a new user using the provided username and password.
        Updates the loginPlayerID with the new user ID.

        Parameters:
        username (str): The username of the new user.
        password (str): The password for the new user.
        """
        self.loginPlayerID = self.userManager.create_user(username, password)
        return self.loginPlayerID

    def login_user(self, username, password):
        #use for login button
        """
        Logs in a user with the provided username and password.
        Updates the loginPlayerID with the user ID.

        Parameters:
        username (str): The username of the user attempting to log in.
        password (str): The password of the user attempting to log in.
        """
        self.loginPlayerID = self.userManager.login_user(username, password)
        return self.loginPlayerID

    def check_ratings_exist(self, user_id):
        #use after login and opponent user are confirmed
        """
        Ensures that a ratings record exists for the specified user.
        Creates a rating record if one does not already exist.

        Parameters:
        user_id (str): The user ID for whom to check or create a rating record.
        """
        self.ratingManager.create_rating(user_id)

    def update_game_state(self, game_id, new_game_state):
        #use to update game state in database after moves
        """
        Updates the game state in the database for a given game ID.

        Parameters:
        game_id (str): The ID of the game to update.
        new_game_state (dict): A dictionary representing the new state of the game.
        """       
        self.gameManager.update_game_state(game_id, new_game_state)

    def get_game_state(self, game_id):
        #use to pull game state from database between moves
        """
        Retrieves the current game state from the database for a given game ID.

        Parameters:
        game_id (str): The ID of the game whose state is to be retrieved.

        Returns:
        dict: The current state of the game.
        """        
        return self.gameManager.get_game_state(game_id)

    def create_game(self, gameState):
        #use to create a game with passed in game state from model when game config items are selected
        """
        Creates a new game with the provided game state, setting the game ID after creation.

        Parameters:
        gameState (dict): A dictionary representing the initial state of the game.
        """        
        self.gameID = self.gameManager.create_game(self.loginPlayerID, self.OpponentPlayerID, gameState)

    def update_ratings_win(self, winner_id, loser_id, topScore):
        #use to update ratings for both players once a game is over and one player has won
        """
        Updates the ratings for both players when a game concludes with a winner.

        Parameters:
        winner_id (str): The ID of the player who won the game.
        loser_id (str): The ID of the player who lost the game.
        topScore (int): The top score achieved in the game, used to update the rating.
        """        
        self.ratingManager.update_top_score(winner_id, topScore)
        self.ratingManager.update_wins(winner_id)
        self.ratingManager.update_losses(loser_id)
        self.ratingManager.update_elo_rating(winner_id, self.ratingManager.get_elo_rating(loser_id), 1)
        self.ratingManager.update_elo_rating(loser_id, self.ratingManager.get_elo_rating(winner_id), -1)

    def update_ratings_draw(self, player1_id, player2_id):
        #use to update ratings for both players once a game is over and it ends in a tie
        """
        Updates the ratings for both players when a game concludes with a draw.

        Parameters:
        player1_id (str): The ID of the first player.
        player2_id (str): The ID of the second player.
        """        
        self.ratingManager.update_ties(player1_id)
        self.ratingManager.update_ties(player2_id)
        self.ratingManager.update_elo_rating(player1_id, self.ratingManager.get_elo_rating(player2_id), 0)
        self.ratingManager.update_elo_rating(player2_id, self.ratingManager.get_elo_rating(player1_id), 0)