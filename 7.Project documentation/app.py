"""
OptiCrop backend entrypoint.
Run with: python app.py
"""
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
for path in (ROOT_DIR, BASE_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)


def _ensure_runtime_dependencies():
    try:
        import flask  # noqa: F401
    except ModuleNotFoundError:
        requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
        print("[OptiCrop] Flask dependency missing. Installing backend requirements into the current Python environment...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(
                "Could not install backend requirements automatically. Please run 'python -m pip install -r backend/requirements.txt' manually."
            ) from exc


_ensure_runtime_dependencies()

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash

from backend.config import Config
from backend.database.db import init_db
from backend.models.user import User
from backend.routes.auth import auth_bp
from backend.routes.crops import crops_bp
from backend.routes.weather import weather_bp
from backend.routes.prediction import prediction_bp
from backend.routes.disease import disease_bp
from backend.routes.market import market_bp
from backend.routes.datasets import datasets_bp


def _initialize_database_and_seed_demo_user():
    init_db()
    if not User.find_by_email("demo@example.com"):
        User.create("Demo User", "demo@example.com", generate_password_hash("demo123"))


_initialize_database_and_seed_demo_user()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    JWTManager(app)

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        return response

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(crops_bp, url_prefix="/api/crops")
    app.register_blueprint(weather_bp, url_prefix="/api/weather")
    app.register_blueprint(prediction_bp, url_prefix="/api/prediction")
    app.register_blueprint(disease_bp, url_prefix="/api/disease")
    app.register_blueprint(market_bp, url_prefix="/api/market")
    app.register_blueprint(datasets_bp, url_prefix="/api/datasets")

    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "OptiCrop API"})

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)
