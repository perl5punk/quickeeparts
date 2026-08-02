import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from app.junk_item import JunkItem


def create_app(testing=False):
    """Application factory."""
    app.config['TESTING'] = testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), '..', 'instance', 'quickeeparts.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'

    # Ensure static directories exist
    upload_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
    thumb_dir = os.path.join(upload_dir, 'thumbnails')
    images_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'images')
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(thumb_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    return app


def init_db_for_app(app_inst):
    """Initialize database for a given app instance."""
    with app_inst.app_context():
        db.drop_all()
        db.create_all()


if __name__ == '__main__':
    a = create_app()
    init_db_for_app(a)
    a.run(debug=True)
