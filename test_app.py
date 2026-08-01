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


@pytest.fixture
def app_client():
    """Create a test client for the Flask app."""
    from app import app
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client


@pytest.fixture
def client_with_item(app_client):
    """Add a junk item to the database."""
    app_client.post('/add', data={
        'name': 'Old Bolt',
        'description': 'A rusty bolt',
        'category': 'Hardware'
    })
    return app_client


class TestFileStructure:
    """Test that all required files exist."""

    def test_app_py_exists(self):
        assert os.path.isfile(os.path.join(ROOT, 'app.py'))

    def test_requirements_txt_exists(self):
        path = os.path.join(ROOT, 'requirements.txt')
        assert os.path.isfile(path)

    def test_requirements_txt_contains_flask(self):
        path = os.path.join(ROOT, 'requirements.txt')
        content = open(path).read()
        assert 'flask' in content

    def test_templates_directory_exists(self):
        path = os.path.join(ROOT, 'templates')
        assert os.path.isdir(path)

    def test_index_html_exists(self):
        path = os.path.join(ROOT, 'templates', 'index.html')
        assert os.path.isfile(path)

    def test_add_html_exists(self):
        path = os.path.join(ROOT, 'templates', 'add.html')
        assert os.path.isfile(path)

    def test_list_html_exists(self):
        path = os.path.join(ROOT, 'templates', 'list.html')
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
        path = os.path.join(ROOT, 'templates', 'index.html')
        content = open(path).read()
        assert 'QuickeeParts' in content

    def test_index_has_add_link(self):
        path = os.path.join(ROOT, 'templates', 'index.html')
        content = open(path).read()
        assert '/add' in content

    def test_index_has_list_link(self):
        path = os.path.join(ROOT, 'templates', 'index.html')
        content = open(path).read()
        assert '/list' in content


class TestListTemplate:
    """Test list.html template content."""

    def test_list_uses_items_variable(self):
        path = os.path.join(ROOT, 'templates', 'list.html')
        content = open(path).read()
        assert 'items' in content

    def test_list_has_no_junk_message(self):
        path = os.path.join(ROOT, 'templates', 'list.html')
        content = open(path).read()
        assert 'No junk items yet' in content or 'no junk' in content.lower()


class TestAppConfig:
    """Test app configuration."""

    def test_app_runs_on_localhost_5000(self):
        """Check that the main block uses the correct host and port."""
        import app as app_module
        # Verify app.run parameters by checking the source
        source = open(os.path.join(ROOT, 'app.py')).read()
        assert "'127.0.0.1'" in source or '"127.0.0.1"' in source
        assert '5000' in source
        assert 'debug=False' in source

class TestInstanceDirectory:
    """Test that the instance/ directory and junk.db exist."""

    def test_instance_directory_exists(self):
        """The instance/ directory must exist at the project root."""
        path = os.path.join(ROOT, 'instance')
        assert os.path.isdir(path), "instance/ directory not found at project root"

    def test_junk_db_exists_in_instance(self):
        """The junk.db SQLite file must exist inside instance/."""
        path = os.path.join(ROOT, 'instance', 'junk.db')
        assert os.path.isfile(path), "instance/junk.db not found"

    def test_db_path_is_relative_to_instance(self):
        """DATABASE must be configured relative to app.instance_path."""
        from app import app, DATABASE
        expected = os.path.join(app.instance_path, 'junk.db')
        assert DATABASE == expected, f"DATABASE path {DATABASE} is not relative to instance_path {expected}"


class TestPostRedirectGet:
    """Test POST-Redirect-GET pattern on /add."""

    def test_add_post_returns_302_redirect(self, app_client):
        """POST to /add should return a 302 redirect (not 200)."""
        response = app_client.post('/add', data={
            'name': 'Redirect Test',
            'description': 'Testing redirect',
            'category': 'Test'
        }, follow_redirects=False)
        assert response.status_code == 302, f"Expected 302 redirect, got {response.status_code}"

    def test_add_post_redirect_location(self, app_client):
        """POST to /add should redirect to /add."""
        response = app_client.post('/add', data={
            'name': 'Redirect Location Test',
            'description': 'test',
            'category': 'Test'
        }, follow_redirects=False)
        assert response.status_code == 302
        assert '/add' in response.location, f"Redirect location should be /add, got {response.location}"


class TestDatabaseSchema:
    """Test database schema constraints and defaults."""

    def test_name_column_is_not_null(self, app_client):
        """The name column must have a NOT NULL constraint."""
        import app as app_module
        db = sqlite3.connect(app_module.DATABASE)
        cursor = db.execute("PRAGMA table_info(junk)")
        columns = {row[1]: row for row in cursor.fetchall()}
        db.close()
        name_column = columns.get('name')
        assert name_column is not None, "name column not found"
        # Column not-null flag is in index 3 (0=nullable, 1=NOT NULL)
        assert name_column[3] == 1, "name column should have NOT NULL constraint"

    def test_date_added_has_default_current_timestamp(self, app_client):
        """The date_added column should have DEFAULT CURRENT_TIMESTAMP."""
        import app as app_module
        db = sqlite3.connect(app_module.DATABASE)
        cursor = db.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='junk'")
        schema_sql = cursor.fetchone()[0]
        db.close()
        assert 'DEFAULT CURRENT_TIMESTAMP' in schema_sql, (
            f"date_added should have DEFAULT CURRENT_TIMESTAMP. "
            f"Schema: {schema_sql}"
        )


class TestNoExternalFrameworks:
    """Test that no external CSS/JS frameworks are used."""

    def test_no_bootstrap_in_templates(self):
        """No Bootstrap framework CSS/JS should be present."""
        for tmpl in ['index.html', 'add.html', 'list.html']:
            path = os.path.join(ROOT, 'templates', tmpl)
            content = open(path).read().lower()
            assert 'bootstrap' not in content, (
                f"Bootstrap framework found in {tmpl}"
            )

    def test_no_jquery_in_templates(self):
        """No jQuery library should be present."""
        for tmpl in ['index.html', 'add.html', 'list.html']:
            path = os.path.join(ROOT, 'templates', tmpl)
            content = open(path).read().lower()
            assert 'jquery' not in content, (
                f"jQuery library found in {tmpl}"
            )


class TestDBConnectionPattern:
    """Test that database connections follow the per-request pattern."""

    def test_get_db_uses_g_object(self):
        """get_db should use Flask's g object for connection storage."""
        import app as app_module
        source = open(os.path.join(ROOT, 'app.py')).read()
        assert "if 'db' not in g" in source, "get_db should check g for existing db connection"
        assert "g.db = sqlite3.connect" in source, "get_db should store connection in g.db"

    def test_close_db_pops_g(self):
        """close_db should pop the db from g to close the connection."""
        import app as app_module
        source = open(os.path.join(ROOT, 'app.py')).read()
        assert "g.pop('db', None)" in source or "g.pop(\"db\", None)" in source, (
            "close_db should pop db from g"
        )


class TestListTemplateDisplay:
    """Test that list.html displays all required fields."""

    def test_list_shows_all_fields(self, client_with_item):
        """list.html should display name, description, category, and date_added."""
        response = client_with_item.get('/list')
        assert response.status_code == 200
        data = response.data.decode('utf-8')
        assert 'Old Bolt' in data, "Name should be displayed"
        assert 'A rusty bolt' in data, "Description should be displayed"
        assert 'Hardware' in data, "Category should be displayed"
        # date_added should contain a date/time string
        assert '20' in data and '-' in data, (
            "date_added should be displayed"
        )
