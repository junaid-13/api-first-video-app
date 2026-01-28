from datetime import datetime, timedelta
from app.extensions import mongo

class RefreshToken:
    @staticmethod
    def create(user_id, token_hash, ip=None, user_agent=None):
        doc = {
            "user_id": user_id,
            "token_hash": token_hash,
            "ip_address": ip,
            "user_agent": user_agent,
            "revoked": False,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(days=7)
        }
        mongo.db.refresh_tokens.insert_one(doc)

    @staticmethod
    def find_by_token_hash(token_hash):
        return mongo.db.refresh_tokens.find_one({
            "token_hash": token_hash
        })

    @staticmethod
    def revoke(token_id):
        mongo.db.refresh_tokens.update_one(
            {"_id": token_id},
            {"$set": {"revoked": True}}
        )

    @staticmethod
    def revoke_all_for_user(user_id):
        if user_id:
            mongo.db.refresh_tokens.update_many(
                {"user_id": user_id},
                {"$set": {"revoked": True}}
            )
