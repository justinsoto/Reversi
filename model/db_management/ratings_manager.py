import mysql.connector

class Rating:
    def __init__(self, user_id, top_score, number_wins, number_losses) -> None:
        self.user_id = user_id
        self.top_score = top_score
        self.number_wins = number_wins
        self.number_losses = number_losses

    def get_user_id(self):
        return self.user_id
    #Probably need to add a display method for the rating class

class RatingsManager:
    def __init__(self, connection):
        self.connection = connection

    def create_rating(self, top_score, number_wins, number_losses):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Ratings (Top_Score, Number_Wins, Number_Loses) VALUES (%s, %s, %s)"
            cursor.execute(query, (top_score, number_wins, number_losses))
            self.connection.commit()

            cursor.execute("SELECT LAST_INSERT_ID()")
            last_id_tuple = cursor.fetchone()
            last_id = last_id_tuple[0]
            self.curr_rating = Rating(last_id, top_score, number_wins, number_losses)
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
                return Rating(rating_data['User_ID'], rating_data['Top_Score'], rating_data['Number_Wins'], rating_data['Number_Loses'])
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
