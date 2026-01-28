from flask import Blueprint, jsonify
from app.utils.security import jwt_required

video_bp = Blueprint("video", __name__, url_prefix="/api/v1")

@video_bp.route("/dashboard", methods=["GET"])
@jwt_required
def dashboard():
    return jsonify({
        "message": "Dashboard access granted"
    })
