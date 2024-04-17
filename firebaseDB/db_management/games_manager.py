import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

class GamesManager():
    def __init__(self, db):
        """
        Initializes the GamesManager with a reference to the Firestore database.

        Parameters:
        db (firestore.client): The Firestore database client instance.
        """        
        self.db = db
        self.col_ref = self.db.collection('GameCollection')

    def check_game_exists(self, player1_id, player2_id):
        """
        Checks if a game between two specified players exists in the database.

        Parameters:
        player1_id (str): The ID of the first player.
        player2_id (str): The ID of the second player.

        Returns:
        str/bool: Returns the game ID if found, False otherwise.
        """        
        filter1 = FieldFilter("Player1_ID", "==", str(player1_id))
        filter2 = FieldFilter("Player2_ID", "==", str(player2_id))

        query_ref = self.col_ref.where(filter = filter1).where(filter = filter2).get()
        for doc in query_ref:
            if doc:
                return doc.id
            else:
                print("Game not Found")
                return False

    def create_game(self, player1_id, player2_id, game_state):
        """
        Creates a new game in the database with the given state if it doesn't already exist between the two players.

        Parameters:
        player1_id (str): The ID of the first player.
        player2_id (str): The ID of the second player.
        game_state (dict): The initial state of the game.

        Returns:
        str/bool: Returns the newly created game ID if successful, False otherwise.
        """        
        doc_ref = self.col_ref.document()
        if self.check_game_exists(player1_id, player2_id):
            print("Game already exists")
            return False
        data = {
                "Player1_ID": str(player1_id),
                "Player2_ID": str(player2_id),
                "Game_State": game_state
            }

        doc_ref.set(data)
        return doc_ref.id

    def delete_game(self, game_id):
        """
        Deletes a game from the database by its ID.

        Parameters:
        game_id (str): The ID of the game to delete.
        """        
        temp_ref = self.col_ref.document(game_id)
        doc = temp_ref.get()
        if doc:
            temp_ref.delete()
            print(f"Game {game_id} has been deleted successfully.")
        else:
            print("Game could not be found")

    def update_game_state(self, game_id, new_game_state):
        """
        Updates the state of a game in the database.

        Parameters:
        game_id (str): The ID of the game to update.
        new_game_state (dict): The new state to update the game with.
        """        
        doc_ref = self.col_ref.document(game_id)
        doc_ref.update({"Game_State": new_game_state})
        print("Game state updated")

    def get_game_state(self, game_id):
        """
        Retrieves the state of a game from the database by its ID.

        Parameters:
        game_id (str): The ID of the game.

        Returns:
        dict/bool: Returns the current state of the game if found, False otherwise.
        """        
        doc_ref = self.col_ref.document(game_id)
        doc = doc_ref.get()
        if doc:
            data = doc.to_dict()
            return data.get('Game_State')
        else:
            print("Could not get game state")
            return False

    def get_game(self, game_id):
        """
        Retrieves the complete game data from the database by its ID.

        Parameters:
        game_id (str): The ID of the game.

        Returns:
        dict/bool: Returns the complete game data if found, False otherwise.
        """        
        doc_ref = self.col_ref.document(game_id)
        doc = doc_ref.get()
        if doc:
            return dict(sorted(doc.to_dict().items()))
        else:
            print(f"Game {game_id} does not exist")
            return False