"""Fixtures for photo upload tests."""
import os
import pytest


@pytest.fixture(autouse=True)
def _clean_junk_item_table():
    """Clear the junk_item table and reset autoincrement before each test."""
    from app import app
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
