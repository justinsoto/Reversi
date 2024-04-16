import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

class UserManager():
    def __init__(self):
        #Change filepath to your file's path
        self.cred = credentials.Certificate(r"firebaseDB\softwareengineeringproje-b3db3-firebase-adminsdk-5k21y-3119caacb7.json")
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        self.col_ref = self.db.collection('UserCollection')


    def create_user(self, username, password):
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
        if self.check_username_exists(username):
            filter = FieldFilter("Password", "==", str(password))
            query_ref = self.col_ref.where(filter = filter).get()
            for doc in query_ref:
                if doc:
                    print("Username/Password Combo is valid")
                    return doc.id
            print("Password is incorrect")
            return False
        else:
            ("Username Doesn't Exist")
            return False

    def get_user_by_id(self, user_id):
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
        id = self.check_username_exists(username)
        if id:
            temp_ref = self.col_ref.document(id)
            temp_ref.delete()
            print(f"User {username} has been deleted successfully.")
        else:
            print("User could not be found")

    def list_current_users(self):
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
