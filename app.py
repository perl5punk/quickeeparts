import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config=None):
    """Application factory that creates and configures the Flask app with database support."""
    app = Flask(__name__)

    # Ensure the instance directory exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Application configuration defaults
    app.config["SECRET_KEY"] = os.urandom(24)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(app.instance_path, "app.db")}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Override with provided config
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        else:
            app.config.from_object(config)

    # Initialize Flask-SQLAlchemy extension with the app
    db.init_app(app)

    @app.route("/")
    def home():
        """Return the QuickeeParts home page."""
        return "<html><body><h1>QuickeeParts — The parts utility</h1></body></html>"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)  # Flask development server
