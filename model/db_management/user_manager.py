import mysql.connector

class User:
    def __init__(self, user_id, username, password_hash) -> None:
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash

class UserManager:
    def __init__(self, connection) -> None:
        self.connection = connection

    def create_user(self, username, password_hash):
        try:
            cursor = self.connection.cursor()
            query= "INSERT INTO Users (Username, Password_Hash) VALUES (%s, %s)"
            cursor.execute(query,(username, password_hash))
            self.connection.commit()
            cursor.close()
            return True
        
        except mysql.connector.Error as err:
             print("Error creating user:", err)
             return False

    def get_user_by_id(self, user_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM Users WHERE User_ID = %s"
            cursor.execute(query, (user_id))
            user_data = cursor.fetchone()
            cursor.close()
            if user_data:
                return User(user_data['User_ID'], user_data['Username'], user_data['Password_Hash']) 
            else:
                return None
            
        except mysql.connector.Error as err:
            print("Error getting User b ID:", err)
            return None
        
    def get_user_by_username(self, username):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM Users WHERE Username = %s"
            cursor.execute(query, (username,))
            user_data = cursor.fetchone()
            cursor.close()
            if user_data:
                print('FOUND') #This is just for now --> need view displays for user
                return User(user_data['User_ID'], user_data['Username'], user_data['Password_Hash'])
            else:
                return None
            
        except mysql.connector.Error as err:
            print("Error getting user by username:", err)
            return None
        

        #More CRUD operations if needed
    