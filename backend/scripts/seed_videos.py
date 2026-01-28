from datetime import datetime
from app.extensions import mongo
from app.main import create_app

app = create_app()

videos = [
    {
        "title": "Intro to the App",
        "description": "Welcome video",
        "stream_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "is_active": True,
        "created_at": datetime.utcnow()
    },
    {
        "title": "Advanced Features",
        "description": "Deep dive",
        "stream_url": "https://www.youtube.com/watch?v=9bZkp7q19f0",
        "is_active": True,
        "created_at": datetime.utcnow()
    },
    {
        "title": "Hidden Video",
        "description": "Inactive test",
        "stream_url": "https://www.youtube.com/watch?v=3tmd-ClpJxA",
        "is_active": False,
        "created_at": datetime.utcnow()
    }
]

with app.app_context():
    result = mongo.db.videos.insert_many(videos)
    print("Inserted video IDs:")
    for _id in result.inserted_ids:
        print(_id)
