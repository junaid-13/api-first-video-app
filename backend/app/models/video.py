from app.extensions import mongo
from bson import ObjectId
from bson.errors import InvalidId


class Video:
    @staticmethod
    def find_active():
        return list(
            mongo.db.videos.find(
                {"is_active": True},
                {"stream_url": 0}
            )
        )

    @staticmethod
    def find_active_by_id(video_id):
        try:
            oid = ObjectId(video_id)
        except InvalidId:
            return None   # <-- THIS is the key line

        return mongo.db.videos.find_one({
            "_id": oid,
            "is_active": True
        })
