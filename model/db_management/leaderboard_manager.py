import mysql.connector

class Leaderboard:
    def __init__(self, leaderbaord_id, user_id, top_score, game_id) -> None:
        self.leaderbaord_id = leaderbaord_id
        self.user_id = user_id
        self.top_score = top_score
        self.game_id = game_id

class LeaderboardManager:
    def __init__(self, connection):
        self.connection = connection

    def create_leaderboard_entry(self, user_id, top_score, game_id):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Leaderboard (User_ID, Top_Score, Game_ID) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_id, top_score, game_id))
            self.connection.commit()
            cursor.close()

        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                print("Error: Duplicate entry for the same top score from the same game.")
            else:
                print("Error creating leaderboard entry:", err)

    def get_leaderboard(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Leaderboard ORDER BY Top_Score DESC LIMIT 10")
            leaderboard = cursor.fetchall()
            return leaderboard
        
        except mysql.connector.Error as err:
            print("Error fetching leaderboard entries:", err)

    def update_leaderboard_entry(self, leaderbaord_id, new_top_score):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE Leaderboard SET Top_Score = %s WHERE Leaderboard_ID = %s"
            cursor.execute(query, (new_top_score, leaderbaord_id))
            self.connection.commit()
            cursor.close()

        except mysql.connector.Error as err:
            print("Error updating leaderboard:", err)

    def delete_leaderboard_entry(self, leaderbaord_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Leaderboard WHERE Leaderboard_ID = %s"
            cursor.execute(query, (leaderbaord_id,))
            self.connection.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Error deleting leaderboard:", err)