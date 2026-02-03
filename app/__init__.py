import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name="default"):
    """Application factory pattern."""
    app = Flask(__name__)

    # Load configuration
    from config import config

    app.config.from_object(config[config_name])

    # Ensure upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app import routes

    app.register_blueprint(routes.bp)

    # Import models so they're registered with SQLAlchemy
    from app import models

    return app
