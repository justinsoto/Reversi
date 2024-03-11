import mysql.connector

class Game_DB: #maybe we add a timestamp field?
    def __init__(self, game_id, player1_id, player2_id, winner_id) -> None:
        self.game_id = game_id
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.winner_id = winner_id

class GamesManager:
    def __init__(self, connection) -> None:
        self.connection = connection

    def create_game(self, player1_id, player2_id):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Games (Player1_ID, Player2_ID) VALUES (%s, %s)"
            cursor.execute(query, (player1_id, player2_id))
            self.connection.commit()
            cursor.close()
            return cursor.lastrowid  # Return the ID of the newly inserted game
        
        except mysql.connector.Error as err:
            print("Error creating game:", err)
            return None

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

    #need to have a way to store game id then update once game ends
    def update_winner(self, game_id, winner_id):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE Games SET Winner_ID = %s WHERE Game_ID = %s"
            cursor.execute(query, (winner_id, game_id))
            self.connection.commit()
            cursor.close()
            
        except mysql.connector.Error as err:
            print("Error updating winner:", err)


    def delete_game(self, game_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Games WHERE Game_ID = %s"
            cursor.execute(query, (game_id,))
            self.connection.commit()
            cursor.close()

        except mysql.connector.Error as err:
            print("Error deleting game:", err)