from database.db_management.user_manager import UserManager
import mysql.connector

class LoginDecorator(UserManager):
    def __init__(self, connection, user_manager):
        self.connection = connection
        self.user_manager = user_manager

    def login(self, username, password_hash):
        try:
            cursor = self.connection.cursor(buffered=True)
            query = "SELECT * FROM Users WHERE Username = %s AND Password_Hash = %s"
            cursor.execute(query, (username, password_hash))
            self.connection.commit()
            result = cursor.fetchone()
            cursor.close()

            if result:
                return result[0]
            else:
                return False

        except mysql.connector.Error as err:
            print("Error checking user existence:", err)
            return False
