from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__)

    # Default configuration
    app.config['SECRET_KEY'] = 'fallback-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Override with provided config
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        else:
            app.config.from_object(config)

    # Initialize Flask-SQLAlchemy with the app
    db.init_app(app)

    # Create database tables within app context
    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return 'QuickeeParts — The parts utility'

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
