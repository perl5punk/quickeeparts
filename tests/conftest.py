"""Fixtures for photo upload tests that need a clean junk_item table."""
import os
import pytest


@pytest.fixture(autouse=True)
def clean_junk_item_table(app_client):
    """Clear the junk_item table and reset autoincrement before each test."""
    from app.models import db
    # Clear all rows from the junk_item table
    db.session.query(db.Model).filter(
        db.Model.__tablename__ == 'junk_item'
    ).delete(synchronize_session='fetch')
    db.session.commit()

    # Also clear uploads to keep disk clean
    upload_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'static', 'uploads'
    )
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
