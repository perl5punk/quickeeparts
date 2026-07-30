import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from app.junk_item import JunkItem


def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        print("Database initialized.")


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
