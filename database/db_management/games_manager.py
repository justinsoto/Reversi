import mysql.connector

class Game_DB: #maybe we add a timestamp field?
    def __init__(self, game_id, player1_id, player2_id, winner_id, game_state) -> None:
        self.game_id = game_id
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.winner_id = winner_id
        self.game_state = game_state

    def get_game_id(self):
        return self.game_id

class GamesManager:
    def __init__(self, connection) -> None:
        self.connection = connection

    def create_game(self, player1_id, player2_id):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Games (Player1_ID, Player2_ID) VALUES (%s, %s)"
            cursor.execute(query, (player1_id, player2_id))
            self.connection.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            last_id_tuple = cursor.fetchone()
            last_id = last_id_tuple[0]
            self.curr_game = Game_DB(last_id, player1_id, player2_id, None, None)
            cursor.close()
            return cursor.lastrowid  # Return the ID of the newly inserted game

        except mysql.connector.Error as err:
            print("Error creating game:", err)
            return None

    def get_current_game(self):
        return self.curr_game

    def get_game(self, game_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM Games WHERE Game_ID = %s"
            cursor.execute(query, (game_id,))
            game = cursor.fetchone()
            cursor.close()
            if game:
                print( "FOUND") #just for now
                return Game_DB(game['Game_ID'], game['Player1_ID'], game['Player2_ID'], game['Winner_ID'])
            else:
                return None

        except mysql.connector.Error as err:
            print("Error retrieving game:", err)
            return None

    def delete_game(self, game_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Games WHERE Game_ID = %s"
            cursor.execute(query, (game_id,))
            self.connection.commit()
            cursor.close()

        except mysql.connector.Error as err:
            print("Error deleting game:", err)

    def update_game_state(self, game_id, new_game_state):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE Games SET Game_State = %s WHERE Game_ID = %s"
            cursor.execute(query, (new_game_state, game_id))
            self.connection.commit()
            cursor.close()

        except mysql.connector.Error as err:
            print("Error updating game state:", err)

    def get_game_state(self, game_id):
        try:
            cursor = self.connection.cursor()
            query = "SELECT Game_State FROM Games WHERE Game_ID = %s"
            cursor.execute(query, (game_id,))
            game_state = cursor.fetchone()
            cursor.close()

            if game_state:
                return game_state[0]  # Returning the game state if found
            else:
                return None

        except mysql.connector.Error as err:
            print("Error retrieving game state:", err)
            return None
