import mysql.connector

class Leaderboard:
    def __init__(self, leaderboard_id, user_id, top_score, game_id) -> None:
        self.leaderboard_id = leaderboard_id
        self.user_id = user_id
        self.top_score = top_score
        self.game_id = game_id

    def get_leaderboard_id(self):
        return self.leaderboard_id
    # Probably need to add a display method for the leaderboard class - will call from get leaderboard method?

class LeaderboardManager:
    def __init__(self, connection):
        self.connection = connection

    def create_leaderboard_entry(self, user_id, top_score, game_id):
        # Viraj - I don't know if we need to add the game ID here cause we're going to delete the games once a winner is determined so the gameIDs wont exist
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Leaderboard (User_ID, Top_Score, Game_ID) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_id, top_score, game_id))
            self.connection.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            last_id_tuple = cursor.fetchone()
            last_id = last_id_tuple[0]
            self.curr_leaderboard = Leaderboard(last_id, user_id, top_score, game_id)
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

    def update_leaderboard_entry(self, leaderboard_id, new_top_score):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE Leaderboard SET Top_Score = %s WHERE Leaderboard_ID = %s"
            cursor.execute(query, (new_top_score, leaderboard_id))
            self.connection.commit()
            cursor.close()

        except mysql.connector.Error as err:
            print("Error updating leaderboard:", err)

    def delete_leaderboard_entry(self, leaderboard_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Leaderboard WHERE Leaderboard_ID = %s"
            cursor.execute(query, (leaderboard_id,))
            self.connection.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Error deleting leaderboard:", err)

    def get_current_leaderboard(self):
        return self.curr_leaderboard
