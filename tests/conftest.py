"""Fixtures for photo upload tests."""
import os
import sqlite3
import pytest


@pytest.fixture(autouse=True)
def _clean_junk_item_table():
    """Clear the junk_item table and reset autoincrement before each test."""
    from app import app
    ROOT = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(app.instance_path, 'junk.db')

    # Clear junk_item table using raw SQL (avoids ORM issues)
    with app.app_context():
        conn = sqlite3.connect(db_path)
        conn.execute("DELETE FROM junk_item")
        conn.execute("DELETE FROM sqlite_sequence WHERE name='junk_item'")
        conn.commit()
        conn.close()

    upload_dir = os.path.join(ROOT, 'static', 'uploads')

    # Clean uploads directory (but not images which contains placeholder)
    if os.path.exists(upload_dir):
        for f in os.listdir(upload_dir):
            fp = os.path.join(upload_dir, f)
            try:
                if os.path.isfile(fp):
                    os.remove(fp)
                else:
                    import shutil
                    shutil.rmtree(fp)
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
