"""Pytest fixtures for app testing."""
import os
import sys
import tempfile

# Ensure the repo root is on the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from app import app as flask_app, init_db


@pytest.fixture
def app():
    """Create application for testing."""
    flask_app.config['TESTING'] = True
    flask_app.config['DATABASE'] = tempfile.NamedTemporaryFile(delete=False).name

    with flask_app.app_context():
        init_db()

    yield flask_app

    os.unlink(flask_app.config['DATABASE'])


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
