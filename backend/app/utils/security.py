import bcrypt
import jwt
import uuid
import secrets
import hashlib
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app, g

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )

def create_access_token(user_id: str, email: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=15),
        "iss": "api.videoapp",
        "aud": "mobile",
        "jti": str(uuid.uuid4())
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")

def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)

def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()
def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({
                "error": {
                    "code": "AUTH_REQUIRED",
                    "message": "Authorization token required"
                }
            }), 401

        token = auth_header.split(" ", 1)[1]

        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET"],
                algorithms=["HS256"],
                audience="mobile",
                issuer="api.videoapp"
            )
        except jwt.ExpiredSignatureError:
            return jsonify({
                "error": {
                    "code": "AUTH_EXPIRED",
                    "message": "Access token expired"
                }
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                "error": {
                    "code": "AUTH_INVALID",
                    "message": "Invalid access token"
                }
            }), 401

        # attach identity to request context
        g.user_id = payload["sub"]
        g.email = payload["email"]

        return fn(*args, **kwargs)

    return wrapper