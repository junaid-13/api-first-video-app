import hmac
import hashlib
import time
import urllib.parse
from flask import current_app


def generate_signed_url(base_url: str) -> str:
    expires = int(time.time()) + current_app.config["STREAM_URL_TTL_SECONDS"]

    payload = f"{base_url}{expires}".encode()
    secret = current_app.config["STREAM_SIGNING_SECRET"].encode()

    signature = hmac.new(
        secret,
        payload,
        hashlib.sha256
    ).hexdigest()

    params = {
        "expires": expires,
        "sig": signature
    }

    return f"{base_url}?{urllib.parse.urlencode(params)}"
