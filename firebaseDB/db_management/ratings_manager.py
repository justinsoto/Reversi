import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import math

class RatingsManager():
    def __init__(self, db):
        self.db = db
        self.col_ref = self.db.collection('RatingCollection')

    def check_rating_exists(self, user_id):
        filter1 = FieldFilter("User_ID", "==", str(user_id))
        query_ref = self.col_ref.where(filter = filter1).get()
        for doc in query_ref:
            if doc:
                return doc.id
            else:
                print("Rating not Found")
                return False

    def create_rating(self, user_id, top_score = 0, number_wins = 0, number_losses = 0, elo_rating = 1000, number_ties = 0):
        doc_ref = self.col_ref.document()
        if self.check_rating_exists(user_id):
            print("Rating already exists")
            return False
        data = {
            "User_ID": str(user_id),
            "top_score": top_score,
            "number_wins": number_wins,
            "number_losses": number_losses,
            "elo_rating": elo_rating,
            "number_ties": number_ties
        }
        doc_ref.set(data)
        return doc_ref.id

    def get_rating(self, user_id):
        filter = FieldFilter("User_ID", "==", user_id)
        doc_ref = self.col_ref.where(filter = filter).get()
        for doc in doc_ref:
            if doc:
                return dict(sorted(doc.to_dict().items()))
            else:
                print(f"Rating not found for user {user_id}")
                return False

    def get_elo_rating(self, user_id):
        filter = FieldFilter("User_ID", "==", user_id)
        doc_ref = self.col_ref.where(filter = filter).get()
        for doc in doc_ref:
            if doc:
                return doc.get("elo_rating")
            else:
                print(f"Rating not found for user {user_id}")
                return False

    def update_top_score(self, user_id, score):
        doc_ref = self.col_ref.document(self.check_rating_exists(user_id))
        if score > doc_ref.get().to_dict().get("top_score"):
            doc_ref.update({"top_score": score})
            print("Top Score updated")
        else:
            print("Top score is higher")

    def update_wins(self, user_id):
        doc_ref = self.col_ref.document(self.check_rating_exists(user_id))
        wins = doc_ref.get().to_dict().get("number_wins")
        doc_ref.update({"number_wins": wins + 1})
        print("Increased number of wins by 1")

    def update_losses(self, user_id):
        doc_ref = self.col_ref.document(self.check_rating_exists(user_id))
        losses = doc_ref.get().to_dict().get("number_losses")
        doc_ref.update({"number_losses": losses + 1})
        print("Increased number of losses by 1")

    def update_ties(self, user_id):
        doc_ref = self.col_ref.document(self.check_rating_exists(user_id))
        ties = doc_ref.get().to_dict().get("number_ties")
        doc_ref.update({"number_ties": ties + 1})
        print("Increased number of ties by 1")

    def get_leaderboard(self):
        docs = self.col_ref.stream()
        scores = []

        for doc in docs:
            data = doc.to_dict()
            username = data.get('User_ID')
            score = data.get('top_score')
            rating = data.get('elo_rating')
            scores.append([username, score, rating])

        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        return sorted_scores[:5]

    def update_elo_rating(self, user_id, opponent_elo_rating, result):
        user_elo_rating = self.get_elo_rating(user_id)
        expected_score = 1 / (1 + math.pow(10, (opponent_elo_rating - user_elo_rating) / 400))
        actual_score = 1 if result == 1 else 0.5 if result == 0 else 0
        k_factor = 32  # You can adjust the K-factor based on your ELO rating system's requirements
        new_elo_rating = user_elo_rating + k_factor * (actual_score - expected_score)
        doc_ref = self.col_ref.document(self.check_rating_exists(user_id))
        doc_ref.update({"elo_rating": new_elo_rating})
        print(f"updated elo rating to {new_elo_rating}")

    def delete_rating(self, user_id):
        doc_ref = self.col_ref.document(self.check_rating_exists(user_id))
        doc_ref.delete()
