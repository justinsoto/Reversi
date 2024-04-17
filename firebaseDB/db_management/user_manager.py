import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

class UserManager():
    def __init__(self, db):
        """
        Initializes the UserManager with a reference to the Firestore database.

        Parameters:
        db (firestore.client): The Firestore database client instance.
        """        
        self.db = db
        self.col_ref = self.db.collection('UserCollection')


    def create_user(self, username, password):
        """
        Creates a new user in the database with a specified username and password. Checks if the username already exists before creating.

        Parameters:
        username (str): The username for the new user.
        password (str): The password for the new user.

        Returns:
        str/bool: The document ID of the newly created user if successful, False otherwise.
        """        
        doc_ref = self.col_ref.document()
        try:
            if self.check_username_exists(username):
                print("User already exists")
                return False
            data = {
                    "Username": str(username),
                    "Password": str(password)
                }

            doc_ref.set(data)
            return doc_ref.id
        except Exception as e:
            print("Error updating user:", e)

    def check_username_exists(self, username):
        """
        Checks if a specified username exists in the database.

        Parameters:
        username (str): The username to check.

        Returns:
        str/bool: The document ID of the user if the username exists, False otherwise.
        """        
        filter = FieldFilter("Username", "==", str(username))
        query_ref = self.col_ref.where(filter = filter).get()
        for doc in query_ref:
            if doc:
                print("Username Found")
                return doc.id
            else:
                print("Username not found")
                return False

    def login_user(self, username, password):
        """
        Validates a username and password combination against the database.

        Parameters:
        username (str): The username to validate.
        password (str): The password to validate.

        Returns:
        str/bool: The document ID of the user if the credentials are valid, False otherwise.
        """        
        filter1 = FieldFilter("Username", "==", str(username))
        filter2 = FieldFilter("Password", "==", str(password))
        query_ref = self.col_ref.where(filter = filter1).where(filter = filter2).get()
        for doc in query_ref:
            if doc:
                print("Username/Password Combo is valid")
                return doc.id
            else:
                print("Password is incorrect")
                return False

    def get_user_by_id(self, user_id):
        """
        Retrieves a user by their document ID from the database.

        Parameters:
        user_id (str): The document ID of the user to retrieve.

        Returns:
        str/None: The username of the user if found, None otherwise.
        """        
        # Reference to the document
        temp_ref = self.col_ref.document(user_id)
        # Get the document snapshot
        doc = temp_ref.get()
        # Check if the document exists
        if doc:
            # Get the data from the document
            data = doc.to_dict()
            # Get the value of the username field
            username = data.get('Username')
            return username
        else:
            print(f"User does not exist.")
            return None

    def delete_user(self, username):
        """
        Deletes a user from the database by their username after verifying the username exists.

        Parameters:
        username (str): The username of the user to delete.
        """        
        id = self.check_username_exists(username)
        if id:
            temp_ref = self.col_ref.document(id)
            temp_ref.delete()
            print(f"User {username} has been deleted successfully.")
        else:
            print("User could not be found")

    def list_current_users(self):
        """
        Lists all current users in the database by their usernames.

        Returns:
        list: A list of usernames of all current users.
        """        
        docs = self.col_ref.stream()
        usernames = []

        for doc in docs:
            data = doc.to_dict()
            username = data.get('Username')
            if username:
                usernames.append(username)

        for row in usernames:
            print(row)

        print(usernames)
        return usernames
