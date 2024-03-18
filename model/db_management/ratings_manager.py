import mysql.connector
import math

class Rating:
    def __init__(self, user_id, top_score, number_wins, number_losses, elo_rating) -> None:
        self.user_id = user_id
        self.top_score = top_score
        self.number_wins = number_wins
        self.number_losses = number_losses
        self.elo_rating = elo_rating

    def get_user_id(self):
        return self.user_id
    #Probably need to add a display method for the rating class

class RatingsManager:
    def __init__(self, connection):
        self.connection = connection

    def create_rating(self, top_score, number_wins, number_losses, elo_rating=1000):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Ratings (Top_Score, Number_Wins, Number_Loses, ELO_Rating) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (top_score, number_wins, number_losses, elo_rating))
            self.connection.commit()

            cursor.execute("SELECT LAST_INSERT_ID()")
            last_id_tuple = cursor.fetchone()
            last_id = last_id_tuple[0]
            self.curr_rating = Rating(last_id, top_score, number_wins, number_losses, elo_rating)
            cursor.close()

        except mysql.connector.Error as err:
            print("Error creating rating:", err)

    def get_rating(self, user_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM Ratings WHERE User_ID = %s"
            cursor.execute(query, (user_id,))
            rating_data = cursor.fetchone()
            cursor.close()
            if rating_data:
                return Rating(rating_data['User_ID'], rating_data['Top_Score'], rating_data['Number_Wins'], rating_data['Number_Loses'], rating_data['ELO_Rating'])
            else:
                return None

        except mysql.connector.Error as err:
            print("Error retrieving rating:", err)
            return None

    def update_top_score(self, user_id, new_top_score):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE Ratings SET Top_Score = %s WHERE User_ID = %s"
            cursor.execute(query, (new_top_score, user_id))
            self.connection.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Error updating top score:", err)
            return None

    def update_wins(self, user_id):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE Ratings SET Number_Wins = %s WHERE User_ID = %s"
            cursor.execute(query, (1, user_id))
            self.connection.commit()
            cursor.close()

        except mysql.connector.Error as err:
            print("Error updating number of wins:", err)
            return None

    def update_losses(self, user_id):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE Ratings SET Number_Loses = %s WHERE User_ID = %s"
            cursor.execute(query, (1, user_id))
            self.connection.commit()
            cursor.close()

        except mysql.connector.Error as err:
            print("Error updating number of losses:", err)
            return None

    def get_current_rating(self):
        return self.curr_rating
    
    def get_leaderboard(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Ratings ORDER BY Top_Score DESC LIMIT 5")
            leaderboards = cursor.fetchall()
            return leaderboards

        except mysql.connector.Error as err:
            print("Error fetching leaderboard entries:", err)

    def update_elo_rating(self, user_id, opponent_elo_rating, result):
        try:
            cursor = self.connection.cursor()
            query = "SELECT ELO_Rating FROM Ratings WHERE User_ID = %s"
            cursor.execute(query, (user_id,))
            user_elo_rating = cursor.fetchone()[0]

            expected_score = 1 / (1 + math.pow(10, (opponent_elo_rating - user_elo_rating) / 400))
            actual_score = 1 if result == 1 else 0.5 if result == 0 else 0
            k_factor = 32  # You can adjust the K-factor based on your ELO rating system's requirements

            new_elo_rating = user_elo_rating + k_factor * (actual_score - expected_score)
            query_update_elo = "UPDATE Ratings SET ELO_Rating = %s WHERE User_ID = %s"
            cursor.execute(query_update_elo, (new_elo_rating, user_id))
            self.connection.commit()
            cursor.close()

            self.curr_rating.elo_rating = new_elo_rating  # Update the current rating object as well

        except mysql.connector.Error as err:
            print("Error updating ELO rating:", err)

    def get_elo_rating(self, user_id):
        try:
            cursor = self.connection.cursor()
            query = "SELECT ELO_Rating FROM Ratings WHERE User_ID = %s"
            cursor.execute(query, (user_id,))
            elo_rating = cursor.fetchone()[0]
            cursor.close()
            return elo_rating

        except mysql.connector.Error as err:
            print("Error fetching ELO rating:", err)
            
    def delete_rating(self, user_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Ratings WHERE User_ID = %s"
            cursor.execute(query, (user_id,))
            self.connection.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Error deleting rating:", err)
            return None
