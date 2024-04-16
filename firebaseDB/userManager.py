import firebase_admin
from firebase_admin import credentials, firestore

# cred = credentials.Certificate(r"C:\Users\bhond\Desktop\Reversi\firebaseDB\softwareengineeringproje-b3db3-firebase-adminsdk-5k21y-3119caacb7.json")
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# def update_user(username, password):
#     try:
#         doc_ref = db.collection('UserCollection').document("UikCT80RQhxOmdfOl16w")

#         data = {
#                 "Username": str(username),
#                 "Password": str(password)
#             }

#         doc_ref.update(data)
#         print("User updated successfully")
#     except Exception as e:
#         print("Error updating user:", e)

# def main():
#     update_user("test2", 'test2')

class userManager():
    def __init__(self):
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
