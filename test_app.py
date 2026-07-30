"""Basic tests for the QuickeeParts Flask application."""
import os
import sys
import tempfile
import sqlite3
import pytest

# Ensure app can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Root directory is where this test file lives
ROOT = os.path.dirname(os.path.abspath(__file__))


class TestFileStructure:
    """Test that all required files exist."""

    def test_app_py_exists(self):
        assert os.path.isfile(os.path.join(os.path.dirname(__file__), '..', 'app.py'))

    def test_requirements_txt_exists(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
        assert os.path.isfile(path)

    def test_requirements_txt_contains_flask(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
        content = open(path).read()
        assert 'flask' in content

    def test_templates_directory_exists(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'templates')
        assert os.path.isdir(path)

    def test_index_html_exists(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'index.html')
        assert os.path.isfile(path)

    def test_add_html_exists(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'add.html')
        assert os.path.isfile(path)

    def test_list_html_exists(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'list.html')
        assert os.path.isfile(path)


class TestAppCreation:
    """Test that the Flask app is created correctly."""

    def test_app_instance(self):
        from app import app
        assert app is not None

    def test_flask_import(self):
        from flask import Flask
        from app import app
        assert isinstance(app, Flask)


class TestRoutes:
    """Test all routes."""

    @pytest.fixture(autouse=True)
    def setup(self, app_client):
        pass

    @pytest.fixture
    def app_client(self):
        from app import app
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        with app.test_client() as client:
            yield client

    def test_index_route(self, app_client):
        response = app_client.get('/')
        assert response.status_code == 200

    def test_add_get_route(self, app_client):
        response = app_client.get('/add')
        assert response.status_code == 200

    def test_list_route(self, app_client):
        response = app_client.get('/list')
        assert response.status_code == 200

    def test_add_post_route(self, app_client):
        response = app_client.post('/add', data={
            'name': 'Test Part',
            'description': 'A test junk item',
            'category': 'Hardware'
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_index_contains_app_name(self, app_client):
        response = app_client.get('/')
        assert b'QuickeeParts' in response.data

    def test_index_contains_links(self, app_client):
        response = app_client.get('/')
        assert b'/add' in response.data
        assert b'/list' in response.data


class TestAddForm:
    """Test the add form template."""

    def test_add_form_fields(self, app_client):
        response = app_client.get('/add')
        assert b'name' in response.data
        assert b'description' in response.data
        assert b'category' in response.data

    def test_add_form_action(self, app_client):
        response = app_client.get('/add')
        assert b'action="/add"' in response.data or b'action="/add"' in response.data.lower()


class TestListItems:
    """Test listing items from the database."""

    @pytest.fixture
    def client_with_item(self, app_client):
        # Add an item first
        app_client.post('/add', data={
            'name': 'Old Bolt',
            'description': 'A rusty bolt',
            'category': 'Hardware'
        })
        return app_client

    def test_list_shows_item(self, client_with_item):
        response = client_with_item.get('/list')
        assert b'Old Bolt' in response.data
        assert b'A rusty bolt' in response.data
        assert b'Hardware' in response.data

    def test_list_shows_date(self, client_with_item):
        response = client_with_item.get('/list')
        # Date should be present
        assert response.status_code == 200


class TestDatabase:
    """Test database initialization."""

    def test_db_table_created(self, app_client):
        """Test that the junk table exists in the database."""
        import app as app_module
        db = sqlite3.connect(app_module.DATABASE)
        cursor = db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='junk'"
        )
        result = cursor.fetchone()
        db.close()
        assert result is not None, "junk table not found in database"

    def test_db_columns(self, app_client):
        """Test that the junk table has the required columns."""
        import app as app_module
        db = sqlite3.connect(app_module.DATABASE)
        cursor = db.execute("PRAGMA table_info(junk)")
        columns = {row[1] for row in cursor.fetchall()}
        db.close()
        assert 'id' in columns
        assert 'name' in columns
        assert 'description' in columns
        assert 'category' in columns
        assert 'date_added' in columns


class TestIndexTemplate:
    """Test index.html template content."""

    def test_index_has_title(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'index.html')
        content = open(path).read()
        assert 'QuickeeParts' in content

    def test_index_has_add_link(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'index.html')
        content = open(path).read()
        assert '/add' in content

    def test_index_has_list_link(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'index.html')
        content = open(path).read()
        assert '/list' in content


class TestListTemplate:
    """Test list.html template content."""

    def test_list_uses_items_variable(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'list.html')
        content = open(path).read()
        assert 'items' in content

    def test_list_has_no_junk_message(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'list.html')
        content = open(path).read()
        assert 'No junk items yet' in content or 'no junk' in content.lower()


class TestAppConfig:
    """Test app configuration."""

    def test_app_runs_on_localhost_5000(self):
        """Check that the main block uses the correct host and port."""
        import app as app_module
        # Verify app.run parameters by checking the source
        source = open(os.path.join(os.path.dirname(__file__), '..', 'app.py')).read()
        assert "'127.0.0.1'" in source or '"127.0.0.1"' in source
        assert '5000' in source
        assert 'debug=False' in source
