from flask import Flask
from flask_cors import CORS

from .config import Config
from .extensions import db
from .migrations import migrate_details_options
from .routes import register_blueprints
from .seed import seed_data


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)

    with app.app_context():
        db.create_all()
        seed_data()
        migrate_details_options()

    register_blueprints(app)

    @app.get("/api/health")
    def health_check():
        return {"status": "ok", "service": "driving-exam-booking"}

    return app
