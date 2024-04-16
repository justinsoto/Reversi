import firebase_admin
from firebase_admin import credentials, firestore

class userManager():
    def __init__(self):
        #Change filepath to your file's path
        self.cred = credentials.Certificate(r"firebaseDB\softwareengineeringproje-b3db3-firebase-adminsdk-5k21y-3119caacb7.json")
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        self.doc_ref = self.db.collection('UserCollection').document()


    def create_user(self, username, password):
        try:
            data = {
                    "Username": str(username),
                    "Password": str(password)
                }

            self.doc_ref.set(data)
            return self.doc_ref.id
        except Exception as e:
            print("Error updating user:", e)

def main():
    p = userManager()
    id = p.create_user("test", "test")
    print(id)

if __name__ == "__main__":
    main()
