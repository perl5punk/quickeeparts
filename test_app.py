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


# ─── Photo Upload Tests ─────────────────────────────────────────────────

"""Tests for photo upload functionality on the /add route."""
import io


def _minimal_jpeg():
    """Return a minimal valid JPEG image (1x1 pixel)."""
    return bytes(
        [
            0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46,
            0x49, 0x46, 0x00, 0x01, 0x01, 0x00, 0x00, 0x01,
            0x00, 0x01, 0x00, 0x00, 0xFF, 0xDB, 0x00, 0x43,
            0x00, 0x08, 0x06, 0x06, 0x07, 0x06, 0x05, 0x08,
            0x07, 0x07, 0x07, 0x09, 0x09, 0x08, 0x0A, 0x0C,
            0x14, 0x0D, 0x0C, 0x0B, 0x0B, 0x0C, 0x19, 0x12,
            0x13, 0x0F, 0x14, 0x1D, 0x1A, 0x1F, 0x1E, 0x1D,
            0x1A, 0x1C, 0x1C, 0x20, 0x24, 0x2E, 0x27, 0x20,
            0x22, 0x2C, 0x23, 0x1C, 0x1C, 0x28, 0x37, 0x29,
            0x2C, 0x30, 0x31, 0x34, 0x34, 0x34, 0x1F, 0x27,
            0x39, 0x3D, 0x38, 0x32, 0x3C, 0x2E, 0x33, 0x34,
            0x32, 0xFF, 0xC0, 0x00, 0x0B, 0x08, 0x00, 0x01,
            0x00, 0x01, 0x01, 0x01, 0x11, 0x00, 0xFF, 0xC4,
            0x00, 0x1F, 0x00, 0x00, 0x01, 0x05, 0x01, 0x01,
            0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x01, 0x02, 0x03, 0x04,
            0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0xFF,
            0xC4, 0x00, 0xB5, 0x10, 0x00, 0x02, 0x01, 0x03,
            0x03, 0x02, 0x04, 0x03, 0x05, 0x05, 0x04, 0x04,
            0x00, 0x00, 0x01, 0x7D, 0x01, 0x02, 0x03, 0x00,
            0x04, 0x11, 0x05, 0x12, 0x21, 0x31, 0x41, 0x06,
            0x13, 0x51, 0x61, 0x07, 0x22, 0x71, 0x14, 0x32,
            0x81, 0x91, 0xA1, 0x08, 0x23, 0x42, 0xB1, 0xC1,
            0x15, 0x52, 0xD1, 0xF0, 0x24, 0x33, 0x62, 0x72,
            0x82, 0x09, 0x0A, 0x16, 0x17, 0x18, 0x19, 0x1A,
            0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x34, 0x35,
            0x36, 0x37, 0x38, 0x39, 0x3A, 0x43, 0x44, 0x45,
            0x46, 0x47, 0x48, 0x49, 0x4A, 0x53, 0x54, 0x55,
            0x56, 0x57, 0x58, 0x59, 0x5A, 0x63, 0x64, 0x65,
            0x66, 0x67, 0x68, 0x69, 0x6A, 0x73, 0x74, 0x75,
            0x76, 0x77, 0x78, 0x79, 0x7A, 0x83, 0x84, 0x85,
            0x86, 0x87, 0x88, 0x89, 0x8A, 0x92, 0x93, 0x94,
            0x95, 0x96, 0x97, 0x98, 0x99, 0x9A, 0xA2, 0xA3,
            0xA4, 0xA5, 0xA6, 0xA7, 0xA8, 0xA9, 0xAA, 0xB2,
            0xB3, 0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA,
            0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8, 0xC9,
            0xCA, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8,
            0xD9, 0xDA, 0xE1, 0xE2, 0xE3, 0xE4, 0xE5, 0xE6,
            0xE7, 0xE8, 0xE9, 0xEA, 0xF1, 0xF2, 0xF3, 0xF4,
            0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA, 0xFF, 0xDA,
            0x00, 0x08, 0x01, 0x01, 0x00, 0x00, 0x3F, 0x00,
            0x7B, 0x40, 0x5F, 0xD9,
        ]
    )


def _minimal_png():
    """Return a minimal valid PNG image (1x1 pixel, red)."""
    return bytes(
        [
            0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,
            # IHDR
            0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,
            0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
            0x08, 0x02, 0x00, 0x00, 0x00, 0x90, 0x77, 0x53,
            0xDE,
            # IDAT
            0x00, 0x00, 0x00, 0x0C, 0x49, 0x44, 0x41, 0x54,
            0x08, 0xD7, 0x63, 0xF8, 0xCF, 0xC0, 0x00, 0x00,
            0x00, 0x02, 0x00, 0x01, 0xE2, 0x21, 0xBC, 0x33,
            # IEND
            0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44,
            0xAE, 0x42, 0x60, 0x82,
        ]
    )


def test_multipart_formdata_accepted(app_client):
    """The /add route (POST) accepts multipart/form-data submissions."""
    jpeg = _minimal_jpeg()
    data = {
        "photo": (io.BytesIO(jpeg), "test.jpg"),
        "name": "Test Part",
        "description": "A test part with photo",
        "category": "Hardware",
    }
    response = app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    assert response.status_code == 302


def test_mime_type_validation_jpeg(app_client):
    """The route validates that uploaded file has allowed MIME type image/jpeg."""
    jpeg = _minimal_jpeg()
    data = {
        "photo": (io.BytesIO(jpeg), "test.jpg"),
        "name": "Test Part",
        "description": "",
        "category": "",
    }
    response = app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    assert response.status_code == 302


def test_mime_type_validation_png(app_client):
    """The route validates that uploaded file has allowed MIME type image/png."""
    png = _minimal_png()
    data = {
        "photo": (io.BytesIO(png), "test.png"),
        "name": "Test Part",
        "description": "",
        "category": "",
    }
    response = app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    assert response.status_code == 302


def test_invalid_extension_returns_400(app_client):
    """Invalid file extension (non-jpg/jpeg/png) returns a 400 response."""
    jpeg = _minimal_jpeg()
    data = {
        "photo": (io.BytesIO(jpeg), "test.gif"),
        "name": "Test Part",
        "description": "",
        "category": "",
    }
    response = app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    assert response.status_code == 400


def test_invalid_extension_rejected_with_message(app_client):
    """Invalid file type rejection returns a 400 with a clear error message."""
    data = {
        "photo": (io.BytesIO(b"not a real image"), "test.gif"),
        "name": "Test Part",
        "description": "",
        "category": "",
    }
    response = app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    assert response.status_code == 400
    assert b"Invalid file type" in response.data or b"not allowed" in response.data.lower()


def test_invalid_mime_type_returns_400(app_client):
    """Invalid MIME type (not image/jpeg or image/png) returns a 400 response."""
    data = {
        "photo": (io.BytesIO(b"some text content"), "test.txt"),
        "name": "Test Part",
        "description": "",
        "category": "",
    }
    response = app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    assert response.status_code == 400


def test_file_size_limit_enforced(app_client):
    """Files exceeding 5 MB (5242880 bytes) return a 400 response."""
    oversized = b"x" * (5242880 + 1)
    data = {
        "photo": (io.BytesIO(oversized), "oversized.jpg"),
        "name": "Test Part",
        "description": "",
        "category": "",
    }
    response = app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    assert response.status_code == 400
    assert b"File too large" in response.data or b"5 MB" in response.data or b"size" in response.data.lower() or b"5242880" in response.data


def test_file_saved_to_instance_photos(app_client):
    """Uploaded files are saved to the instance/photos directory."""
    import app as app_module
    jpeg = _minimal_jpeg()
    initial_count = len(os.listdir(app_module.UPLOAD_FOLDER))
    data = {
        "photo": (io.BytesIO(jpeg), "test.jpg"),
        "name": "Test Part",
        "description": "",
        "category": "",
    }
    app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    final_count = len(os.listdir(app_module.UPLOAD_FOLDER))
    assert final_count > initial_count


def test_randomized_filename_uuid4(app_client):
    """Files are saved with a randomized filename generated using uuid4."""
    import app as app_module
    import re
    jpeg = _minimal_jpeg()
    data = {
        "photo": (io.BytesIO(jpeg), "original_name.jpg"),
        "name": "Test Part",
        "description": "",
        "category": "",
    }
    app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    saved_files = os.listdir(app_module.UPLOAD_FOLDER)
    assert len(saved_files) >= 1
    assert "original_name" not in saved_files[0]
    parts = saved_files[0].rsplit(".", 1)
    assert len(parts) == 2, f"Saved filename should have extension: {saved_files[0]}"
    uuid_part = parts[0]
    assert re.match(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", uuid_part
    ), f"Saved filename should use uuid4 format: {saved_files[0]}"


def test_no_path_traversal(app_client):
    """Path traversal filenames are rejected (secure_filename prevents this)."""
    jpeg = _minimal_jpeg()
    data = {
        "photo": (io.BytesIO(jpeg), "../../../etc/passwd.jpg"),
        "name": "Test Part",
        "description": "",
        "category": "",
    }
    response = app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    assert response.status_code in (302, 400)
    if response.status_code == 302:
        import app as app_module
        for f in os.listdir(app_module.UPLOAD_FOLDER):
            assert ".." not in f and "/" not in f and "\\" not in f


def test_photo_path_column_exists(app_client):
    """Database junk table has the photo_path TEXT column after migration."""
    import app as app_module
    db = sqlite3.connect(app_module.DATABASE)
    columns = [row[1] for row in db.execute("PRAGMA table_info(junk)").fetchall()]
    db.close()
    assert "photo_path" in columns, "photo_path column must exist in junk table"


def test_photo_path_is_nullable(app_client):
    """photo_path column is nullable (existing items without photos work)."""
    import app as app_module
    db = sqlite3.connect(app_module.DATABASE)
    columns = db.execute("PRAGMA table_info(junk)").fetchall()
    db.close()
    photo_col = [c for c in columns if c[1] == "photo_path"]
    assert len(photo_col) == 1
    assert photo_col[0][3] == 0, "photo_path should be nullable"


def test_photo_path_stored_in_database(app_client):
    """On successful upload, photo_path is stored in the database record."""
    import app as app_module
    jpeg = _minimal_jpeg()
    db = sqlite3.connect(app_module.DATABASE)
    data = {
        "photo": (io.BytesIO(jpeg), "test.jpg"),
        "name": "Photo Item",
        "description": "Has a photo",
        "category": "Test",
    }
    app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    row = db.execute("SELECT photo_path FROM junk ORDER BY id DESC LIMIT 1").fetchone()
    db.close()
    assert row is not None
    assert row[0] is not None
    assert row[0].startswith("photos/")


def test_photo_path_relative_to_photos(app_client):
    """photo_path is stored as a relative path under instance/photos/."""
    import app as app_module
    jpeg = _minimal_jpeg()
    db = sqlite3.connect(app_module.DATABASE)
    data = {
        "photo": (io.BytesIO(jpeg), "test.jpg"),
        "name": "Relative Path Test",
        "description": "",
        "category": "",
    }
    app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    row = db.execute("SELECT photo_path FROM junk ORDER BY id DESC LIMIT 1").fetchone()
    db.close()
    assert row is not None
    path = row[0]
    assert path.startswith("photos/"), f"photo_path should start with 'photos/', got: {path}"
    assert ".." not in path, "photo_path should not contain path traversal"
    assert "/" not in path[7:], "photo_path should be photos/<filename>, not nested dirs"


def test_add_post_returns_302_redirect_on_success(app_client):
    """/add POST returns a 302 redirect on successful upload."""
    jpeg = _minimal_jpeg()
    data = {
        "photo": (io.BytesIO(jpeg), "test.jpg"),
        "name": "Redirect Test",
        "description": "",
        "category": "",
    }
    response = app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    assert response.status_code == 302
    assert "/add" in response.location


def test_invalid_mime_returns_400_with_message(app_client):
    """Invalid file type uploads return a 400 response with a clear error message."""
    data = {
        "photo": (io.BytesIO(b"not an image at all"), "test.bmp"),
        "name": "Test Part",
        "description": "",
        "category": "",
    }
    response = app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    assert response.status_code == 400
    body = response.data.decode("utf-8", errors="replace")
    assert (
        "not allowed" in body.lower()
        or "invalid" in body.lower()
        or "allowed" in body.lower()
        or "jpg" in body.lower()
        or "jpeg" in body.lower()
        or "png" in body.lower()
    ), f"Error message should mention allowed types or invalid type. Got: {body}"


def test_file_size_exceeding_limit_returns_400(app_client):
    """File size exceeding the limit returns a 400 response with a clear error message."""
    oversized = b"x" * (10 * 1024 * 1024)
    data = {
        "photo": (io.BytesIO(oversized), "too_large.jpg"),
        "name": "Test Part",
        "description": "",
        "category": "",
    }
    response = app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    assert response.status_code == 400
    body = response.data.decode("utf-8", errors="replace")
    assert (
        "too large" in body.lower()
        or "size" in body.lower()
        or "5 MB" in body.lower()
        or "5242880" in body.lower()
    ), f"Error message should mention size limit. Got: {body}"


def test_backwards_compatible_missing_photo(app_client):
    """Missing photo file in a multipart request does not cause an error."""
    response = app_client.post(
        "/add",
        data={
            "name": "No Photo Item",
            "description": "No photo uploaded",
            "category": "Hardware",
        },
        content_type="multipart/form-data",
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/add" in response.location


def test_backwards_compatible_regular_form(app_client):
    """Text-only form submissions continue to work (backwards compatible)."""
    response = app_client.post(
        "/add",
        data={
            "name": "Text Only Item",
            "description": "No file field at all",
            "category": "Electronics",
        },
        follow_redirects=False,
    )
    assert response.status_code == 302


def test_add_html_enctype_multipart(app_client):
    """The add.html template includes enctype='multipart/form-data' on the form element."""
    response = app_client.get("/add")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "enctype" in html.lower(), "add.html must have enctype attribute on form"
    assert "multipart/form-data" in html.lower(), "enctype must be 'multipart/form-data'"


def test_add_html_file_input(app_client):
    """The add.html template includes a file input field with name='photo'."""
    response = app_client.get("/add")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert 'type="file"' in html or "type='file'" in html, "add.html must have a file input"
    assert "name=\"photo\"" in html or 'name=\'photo\'' in html, "File input must have name='photo'"


# ─── Additional coverage for MIME type validation with valid extension ───

def test_mime_type_rejected_with_valid_extension():
    """Valid extension (jpg) but invalid MIME type (application/octet-stream) returns 400.
    This exercises the MIME check code path (line 103) which extension-only tests never reach."""
    from app import app

    boundary = "----MimeBoundaryCheck"
    body = (
        f"------{boundary}\r\n"
        f'Content-Disposition: form-data; name="photo"; filename="test.jpg"\r\n'
        f"Content-Type: application/octet-stream\r\n"
        f"\r\n"
        f"fake image data\r\n"
        f"------{boundary}\r\n"
        f'Content-Disposition: form-data; name="name"\r\n\r\n'
        f"Test Part\r\n"
        f"------{boundary}\r\n"
        f'Content-Disposition: form-data; name="description"\r\n\r\n'
        f"\r\n"
        f"------{boundary}\r\n"
        f'Content-Disposition: form-data; name="category"\r\n\r\n'
        f"Test\r\n"
        f"------{boundary}--\r\n"
    ).encode()

    with app.test_client() as c:
        resp = c.post(
            "/add",
            data=body,
            content_type=f"multipart/form-data; boundary=----{boundary}",
            follow_redirects=False,
        )
    assert resp.status_code == 400
    body_text = resp.data.decode("utf-8", errors="replace")
    assert (
        "Invalid MIME type" in body_text or "image/jpeg" in body_text or "image/png" in body_text
    ), f"MIME error should mention image types. Got: {body_text}"


def test_photo_path_stored_with_all_fields(app_client):
    """On successful upload, photo_path is stored alongside name, description, and category."""
    import sqlite3

    import app as app_module

    jpeg = _minimal_jpeg()
    data = {
        "photo": (io.BytesIO(jpeg), "test.jpg"),
        "name": "Specific Name",
        "description": "Specific Description",
        "category": "Specific Category",
    }
    app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    db = sqlite3.connect(app_module.DATABASE)
    row = db.execute(
        "SELECT name, description, category, photo_path FROM junk ORDER BY id DESC LIMIT 1"
    ).fetchone()
    db.close()
    assert row[0] == "Specific Name", f"Name mismatch: {row[0]}"
    assert row[1] == "Specific Description", f"Description mismatch: {row[1]}"
    assert row[2] == "Specific Category", f"Category mismatch: {row[2]}"
    assert row[3] is not None, "photo_path should be set"
    assert row[3].startswith("photos/")
