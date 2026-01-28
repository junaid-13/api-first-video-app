import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")

    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv("JWT_ACCESS_EXPIRES")))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv("JWT_REFRESH_EXPIRES")))
    STREAM_SIGNING_SECRET = os.getenv("STREAM_SIGNING_SECRET")
    STREAM_URL_TTL_SECONDS = int(os.getenv("STREAM_URL_TTL_SECONDS", 300))