"""Pytest fixtures for app testing."""
import os
import sys
import tempfile

# Ensure the repo root is on the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest


@pytest.fixture
def client():
    """Create a test client with an isolated database for each test."""
    import app as app_module
    # Use a temporary database file for isolation
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)

    # Override the app's database path
    old_db = app_module.DATABASE
    app_module.DATABASE = db_path

    # Re-initialize the database
    with app_module.app.app_context():
        app_module.init_db()

    app_module.app.config['TESTING'] = True

    client = app_module.app.test_client()

    yield client

    # Restore original database path and clean up
    app_module.DATABASE = old_db
    os.unlink(db_path)
