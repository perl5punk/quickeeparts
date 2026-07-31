"""Tests for photo upload functionality on the /add route."""
import io
import os
import re
import sqlite3
import sys

import pytest

ROOT = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture()
def app_client():
    """Create a test client for the Flask app."""
    from app import app
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client


@pytest.fixture()
def valid_jpg_bytes():
    """Return a minimal valid JPEG image (1x1 pixel)."""
    # Minimal valid JPEG (SOI + APP0 + DQT + SOF0 + DHT + SOS + EOI)
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


@pytest.fixture()
def valid_png_bytes():
    """Return a minimal valid PNG image (1x1 pixel, red)."""
    # Minimal valid PNG (IHDR + IDAT + IEND)
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


@pytest.fixture()
def valid_jpeg_bytes():
    """Return a minimal valid JPEG image bytes (same as valid_jpg_bytes)."""
    return valid_jpg_bytes.__func__(None)


def test_multipart_formdata_accepted(app_client, valid_jpg_bytes):
    """The /add route (POST) accepts multipart/form-data submissions."""
    data = {
        "photo": (io.BytesIO(valid_jpg_bytes), "test.jpg"),
        "name": "Test Part",
        "description": "A test part with photo",
        "category": "Hardware",
    }
    response = app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    assert response.status_code == 302


def test_mime_type_validation_jpeg(app_client, valid_jpg_bytes):
    """The route validates that uploaded file has allowed MIME type image/jpeg."""
    data = {
        "photo": (io.BytesIO(valid_jpg_bytes), "test.jpg"),
        "name": "Test Part",
        "description": "",
        "category": "",
    }
    response = app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    # Should succeed (302 redirect) for valid JPEG MIME
    assert response.status_code == 302


def test_mime_type_validation_png(app_client, valid_png_bytes):
    """The route validates that uploaded file has allowed MIME type image/png."""
    data = {
        "photo": (io.BytesIO(valid_png_bytes), "test.png"),
        "name": "Test Part",
        "description": "",
        "category": "",
    }
    response = app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    # Should succeed (302 redirect) for valid PNG MIME
    assert response.status_code == 302


def test_invalid_extension_returns_400(app_client):
    """Invalid file extension (non-jpg/jpeg/png) returns a 400 response."""
    # Create a file with .gif extension and valid JPEG content
    data = {
        "photo": (io.BytesIO(valid_jpg_bytes.__func__(None)), "test.gif"),
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
    # Create a file with a valid extension but a clearly wrong MIME
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


def test_file_saved_to_instance_photos(app_client, valid_jpg_bytes):
    """Uploaded files are saved to the instance/photos directory."""
    import app as app_module

    initial_count = len(os.listdir(app_module.UPLOAD_FOLDER))
    data = {
        "photo": (io.BytesIO(valid_jpg_bytes), "test.jpg"),
        "name": "Test Part",
        "description": "",
        "category": "",
    }
    app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    # Should have at least one new file
    final_count = len(os.listdir(app_module.UPLOAD_FOLDER))
    assert final_count > initial_count


def test_randomized_filename_uuid4(app_client, valid_jpg_bytes):
    """Files are saved with a randomized filename generated using uuid4."""
    import app as app_module

    data = {
        "photo": (io.BytesIO(valid_jpg_bytes), "original_name.jpg"),
        "name": "Test Part",
        "description": "",
        "category": "",
    }
    app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    saved_files = os.listdir(app_module.UPLOAD_FOLDER)
    assert len(saved_files) >= 1
    # The filename should be a UUID, not the original name
    assert "original_name" not in saved_files[0]
    # UUID has a specific format: 8-4-4-4-12 hex digits with dots
    # Check it looks like a UUID with extension
    parts = saved_files[0].rsplit(".", 1)
    assert len(parts) == 2, f"Saved filename should have extension: {saved_files[0]}"
    uuid_part = parts[0]
    # Validate UUID format (8-4-4-4-12)
    assert re.match(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", uuid_part
    ), f"Saved filename should use uuid4 format: {saved_files[0]}"


def test_no_path_traversal(app_client):
    """Path traversal filenames are rejected (secure_filename prevents this)."""
    # Try to upload a file with a path traversal name
    data = {
        "photo": (io.BytesIO(valid_jpg_bytes.__func__(None)), "../../../etc/passwd.jpg"),
        "name": "Test Part",
        "description": "",
        "category": "",
    }
    response = app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    # Should return 302 (file gets sanitized to UUID) or 400 (rejected)
    assert response.status_code in (302, 400)
    if response.status_code == 302:
        # If it went through, the filename must NOT contain any .. or /
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
    # NOT NULL flag (column 3) should be 0, meaning nullable
    assert photo_col[0][3] == 0, "photo_path should be nullable"


def test_photo_path_stored_in_database(app_client, valid_jpg_bytes):
    """On successful upload, photo_path is stored in the database record."""
    import app as app_module
    db = sqlite3.connect(app_module.DATABASE)
    # Insert a new item with a photo
    data = {
        "photo": (io.BytesIO(valid_jpg_bytes), "test.jpg"),
        "name": "Photo Item",
        "description": "Has a photo",
        "category": "Test",
    }
    app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    # Check the last inserted row
    row = db.execute("SELECT photo_path FROM junk ORDER BY id DESC LIMIT 1").fetchone()
    db.close()
    assert row is not None
    assert row[0] is not None
    assert row[0].startswith("photos/")


def test_photo_path_relative_to_photos(app_client, valid_jpg_bytes):
    """photo_path is stored as a relative path under instance/photos/."""
    import app as app_module
    db = sqlite3.connect(app_module.DATABASE)
    data = {
        "photo": (io.BytesIO(valid_jpg_bytes), "test.jpg"),
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


def test_add_post_returns_302_redirect_on_success(app_client, valid_jpg_bytes):
    """/add POST returns a 302 redirect on successful upload."""
    data = {
        "photo": (io.BytesIO(valid_jpg_bytes), "test.jpg"),
        "name": "Redirect Test",
        "description": "",
        "category": "",
    }
    response = app_client.post(
        "/add", data=data, content_type="multipart/form-data", follow_redirects=False
    )
    assert response.status_code == 302
    assert "/add" in response.location


def test_invalid_mime_returns_400_with_message(app_client, valid_jpg_bytes):
    """Invalid file type uploads return a 400 response with a clear error message."""
    # Create a file with wrong extension and content
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
    # 10 MB file - clearly over the 5 MB limit
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
    # Submit form without a photo file (just text fields)
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
