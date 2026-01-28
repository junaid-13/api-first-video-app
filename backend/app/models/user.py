from datetime import datetime
from bson import ObjectId
from app.extensions import mongo


class User:
    @staticmethod
    def find_by_email(email: str):
        return mongo.db.users.find_one({"email": email})

    @staticmethod
    def find_by_id(user_id):
        return mongo.db.users.find_one({
            "_id": ObjectId(user_id)
        })

    @staticmethod
    def create(name: str, email: str, password_hash: str):
        user = {
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.utcnow(),
        }
        result = mongo.db.users.insert_one(user)
        user["_id"] = result.inserted_id
        return user
