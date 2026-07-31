import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__)

    # Ensure the instance directory exists for SQLite
    os.makedirs(app.instance_path, exist_ok=True)

    # Default configuration
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.instance_path, "app.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Override with provided config
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        else:
            app.config.from_object(config)

    # Initialize Flask-SQLAlchemy with the app
    db.init_app(app)

    @app.route('/')
    def home():
        """Return the QuickeeParts home page."""
        return '<html><body><h1>QuickeeParts — The parts utility</h1></body></html>'

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
# quickeeparts app
