from flask import Blueprint, request, jsonify
from app.models.user import User
from app.utils.security import hash_password
from datetime import datetime


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": {
                "code": "INVALID_REQUEST",
                "message": "Missing JSON body"
            }
        }), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Name, email, and password are required"
            }
        }), 400

    existing_user = User.find_by_email(email)
    if existing_user:
        return jsonify({
            "error": {
                "code": "EMAIL_EXISTS",
                "message": "Email already registered"
            }
        }), 400

    password_hash = hash_password(password)
    user = User.create(name, email, password_hash)

    return jsonify({
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    }), 201

from app.utils.security import (
    verify_password,
    create_access_token,
    generate_refresh_token,
    hash_refresh_token
)
from app.models.refresh_token import RefreshToken

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.find_by_email(email)
    if not user or not verify_password(password, user["password_hash"]):
        return jsonify({
            "error": {
                "code": "INVALID_CREDENTIALS",
                "message": "Invalid email or password"
            }
        }), 401

    access_token = create_access_token(str(user["_id"]), user["email"])
    refresh_token = generate_refresh_token()

    RefreshToken.create(
        user_id=user["_id"],
        token_hash=hash_refresh_token(refresh_token),
        ip=request.remote_addr,
        user_agent=request.headers.get("User-Agent")
    )

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200

@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    data = request.get_json()
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        return jsonify({
            "error": {
                "code": "REFRESH_TOKEN_MISSING",
                "message": "Refresh token required"
            }
        }), 400

    token_hash = hash_refresh_token(refresh_token)

    stored = RefreshToken.find_by_token_hash(token_hash)

    # ❌ Token not found or revoked → reuse or invalid
    if not stored or stored.get("revoked"):
        RefreshToken.revoke_all_for_user(stored["user_id"] if stored else None)
        return jsonify({
            "error": {
                "code": "REFRESH_TOKEN_INVALID",
                "message": "Invalid refresh token"
            }
        }), 401

    # ❌ Expired
    if stored["expires_at"] < datetime.utcnow():
        RefreshToken.revoke(stored["_id"])
        return jsonify({
            "error": {
                "code": "REFRESH_TOKEN_EXPIRED",
                "message": "Refresh token expired"
            }
        }), 401

    # 🔁 ROTATION
    RefreshToken.revoke(stored["_id"])

    new_refresh_token = generate_refresh_token()
    new_refresh_hash = hash_refresh_token(new_refresh_token)

    RefreshToken.create(
        user_id=stored["user_id"],
        token_hash=new_refresh_hash
    )

    user = User.find_by_id(stored["user_id"])

    access_token = create_access_token(str(user["_id"]), user["email"])

    return jsonify({
        "access_token": access_token,
        "refresh_token": new_refresh_token
    }), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    data = request.get_json() or {}
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        return jsonify({
            "error": {
                "code": "REFRESH_TOKEN_REQUIRED",
                "message": "Refresh token is required"
            }
        }), 400

    refresh_hash = hash_refresh_token(refresh_token)
    stored = RefreshToken.find_by_token_hash(refresh_hash)

    if not stored or stored.get("revoked"):
        # Idempotent logout
        return "", 204

    RefreshToken.revoke(stored["_id"])
    return "", 204
