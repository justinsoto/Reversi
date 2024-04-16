import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

class GamesManager():
    def __init__(self):
        #Change filepath to your file's path
        self.cred = credentials.Certificate(r"firebaseDB\softwareengineeringproje-b3db3-firebase-adminsdk-5k21y-3119caacb7.json")
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        self.col_ref = self.db.collection('GameCollection')

    def check_game_exists(self, player1_id, player2_id):
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
        temp_ref = self.col_ref.document(game_id)
        doc = temp_ref.get()
        if doc:
            temp_ref.delete()
            print(f"Game {game_id} has been deleted successfully.")
        else:
            print("Game could not be found")

    def update_game_state(self, game_id, new_game_state):
        doc_ref = self.col_ref.document(game_id)
        doc_ref.update({"Game_State": new_game_state})
        print("Game state updated")

    def get_game_state(self, game_id):
        doc_ref = self.col_ref.document(game_id)
        doc = doc_ref.get()
        if doc:
            data = doc.to_dict()
            return data.get('Game_State')
        else:
            print("Could not get game state")
            return False

    def get_game(self, game_id):
        doc_ref = self.col_ref.document(game_id)
        doc = doc_ref.get()
        if doc:
            return dict(sorted(doc.to_dict().items()))
        else:
            print(f"Game {game_id} does not exist")
            return False
