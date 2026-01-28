from flask import Flask
from .config import Config
from .extensions import mongo, jwt, limiter

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    from .routes.auth import auth_bp
    from .routes.video import video_bp

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(video_bp, url_prefix="/api/v1")

    return app
