import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Module-level database initialization so create_all() runs once at import time
_temp_app = Flask(__name__)
_temp_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
_temp_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with _temp_app.app_context():
    db.init_app(_temp_app)
    db.create_all()


def create_app(config=None):
    app = Flask(__name__)

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
        return '<html><body><h1>QuickeeParts — The parts utility</h1></body></html>'

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
