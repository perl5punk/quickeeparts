"""Fixtures for photo upload tests."""
import os
import pytest


@pytest.fixture(autouse=True)
def _clean_junk_item_table():
    """Clear the junk_item table and reset autoincrement before each test."""
    from app import app

    with app.app_context():
        from app.models import db
        db.session.query(db.Model).filter(
            db.Model.__tablename__ == 'junk_item'
        ).delete(synchronize_session='fetch')
        db.session.commit()

        # Reset SQLite autoincrement counter so next item gets id=1
        db.session.execute(db.text("DELETE FROM sqlite_sequence WHERE name='junk_item'"))
        db.session.commit()

    ROOT = os.path.dirname(os.path.abspath(__file__))
    upload_dir = os.path.join(ROOT, 'static', 'uploads')

    # Clean uploads directory
    if os.path.exists(upload_dir):
        for f in os.listdir(upload_dir):
            fp = os.path.join(upload_dir, f)
            try:
                os.remove(fp)
            except OSError:
                pass
        thumb_dir = os.path.join(upload_dir, 'thumbnails')
        if os.path.exists(thumb_dir):
            for f in os.listdir(thumb_dir):
                fp = os.path.join(thumb_dir, f)
                try:
                    os.remove(fp)
                except OSError:
                    pass

    yield
