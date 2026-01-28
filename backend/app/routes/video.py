from flask import Blueprint, jsonify
from app.utils.security import jwt_required
from app.models.video import Video


video_bp = Blueprint("video", __name__, url_prefix="/api/v1")

@video_bp.route("/dashboard", methods=["GET"])
@jwt_required
def dashboard():
    videos = Video.find_active()

    for v in videos:
        v["_id"] = str(v["_id"])

    return jsonify({
        "videos": videos
    })
@video_bp.route("/video/<video_id>/stream", methods=["GET"])
@jwt_required
def stream(video_id):
    video = Video.find_active_by_id(video_id)

    if not video:
        return jsonify({
            "error": {
                "code": "VIDEO_NOT_FOUND",
                "message": "Video not found"
            }
        }), 404

    # backend redirect (no proxying)
    return redirect(video["stream_url"], code=302)