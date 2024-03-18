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

    def create_leaderboard_entry(self, user_id, top_score, number_wins, number_losses):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Leaderboard (User_ID, Top_Score, Number_Wins, Number_Loses) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (user_id, top_score, number_wins, number_losses))
            self.connection.commit()
            cursor.close()

        except mysql.connector.Error as err:
            print("Error creating leaderboard entry:", err)

    def get_leaderboard(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Leaderboard ORDER BY Top_Score DESC LIMIT 5")
            leaderboards = cursor.fetchall()
            return leaderboards

        except mysql.connector.Error as err:
            print("Error fetching leaderboard entries:", err)

    def update_leaderboard_entry(self, leaderboard_id, new_top_score, new_number_wins, new_number_losses):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE Leaderboard SET Top_Score = %s, Number_Wins = %s, Number_Loses = %s WHERE Leaderboard_ID = %s"
            cursor.execute(query, (new_top_score, new_number_wins, new_number_losses, leaderboard_id))
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
            print("Error deleting leaderboard entry:", err)

    def get_current_leaderboard(self):
        return self.curr_leaderboard
