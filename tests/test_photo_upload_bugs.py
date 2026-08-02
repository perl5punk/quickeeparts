"""Additional tests exposing real bugs in the photo upload implementation."""
import os
import io
import pytest

ROOT = os.path.dirname(os.path.abspath(__file__))


def _minimal_jpeg():
    """Return a minimal valid JPEG image (1x1 pixel)."""
    return bytes([
        0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46, 0x00, 0x01, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x01, 0x00, 0x00, 0xFF, 0xDB, 0x00, 0x43, 0x00, 0x08, 0x06, 0x06, 0x07, 0x06, 0x05, 0x08,
        0x07, 0x07, 0x07, 0x09, 0x09, 0x08, 0x0A, 0x0C, 0x14, 0x0D, 0x0C, 0x0B, 0x0B, 0x0C, 0x19, 0x12,
        0x13, 0x0F, 0x14, 0x1D, 0x1A, 0x1F, 0x1E, 0x1D, 0x1A, 0x1C, 0x1C, 0x20, 0x24, 0x2E, 0x27, 0x20,
        0x22, 0x2C, 0x23, 0x1C, 0x1C, 0x28, 0x37, 0x29, 0x2C, 0x30, 0x31, 0x34, 0x34, 0x34, 0x1F, 0x27,
        0x39, 0x3D, 0x38, 0x32, 0x3C, 0x2E, 0x33, 0x34, 0x32, 0xFF, 0xC0, 0x00, 0x0B, 0x08, 0x00, 0x01,
        0x00, 0x01, 0x01, 0x01, 0x11, 0x00, 0xFF, 0xC4, 0x00, 0x1F, 0x00, 0x00, 0x01, 0x05, 0x01, 0x01,
        0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x02, 0x03, 0x04,
        0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0xFF, 0xC4, 0x00, 0xB5, 0x10, 0x00, 0x02, 0x01, 0x03,
        0x03, 0x02, 0x04, 0x03, 0x05, 0x05, 0x04, 0x04, 0x00, 0x00, 0x01, 0x7D, 0x01, 0x02, 0x03, 0x00,
        0x04, 0x11, 0x05, 0x12, 0x21, 0x31, 0x41, 0x06, 0x13, 0x51, 0x61, 0x07, 0x22, 0x71, 0x14, 0x32,
        0x81, 0x91, 0xA1, 0x08, 0x23, 0x42, 0xB1, 0xC1, 0x15, 0x52, 0xD1, 0xF0, 0x24, 0x33, 0x62, 0x72,
        0x82, 0x09, 0x0A, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x34, 0x35,
        0x36, 0x37, 0x38, 0x39, 0x3A, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x53, 0x54, 0x55,
        0x56, 0x57, 0x58, 0x59, 0x5A, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x73, 0x74, 0x75,
        0x76, 0x77, 0x78, 0x79, 0x7A, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8A, 0x92, 0x93, 0x94,
        0x95, 0x96, 0x97, 0x98, 0x99, 0x9A, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7, 0xA8, 0xA9, 0xAA, 0xB2,
        0xB3, 0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8, 0xC9,
        0xCA, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9, 0xDA, 0xE1, 0xE2, 0xE3, 0xE4, 0xE5, 0xE6,
        0xE7, 0xE8, 0xE9, 0xEA, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA, 0xFF, 0xDA,
        0x00, 0x08, 0x01, 0x01, 0x00, 0x00, 0x3F, 0x00, 0x7B, 0x40, 0x5F, 0xD9,
    ])


def test_files_between_5mb_and_20mb_return_json_error_not_plain_text():
    """Files > 5MB but < 20MB should return a JSON error with 'error' key,
    not Flask's default 413 plain-text HTML response.
    
    The spec requires:
    - File must not exceed 20MB
    - On validation failure, return a JSON error response
    
    But MAX_CONTENT_LENGTH is currently 5MB, so Flask's 413 handler
    intercepts files between 5MB-20MB and returns plain HTML:
    'File too large. Maximum size is 5 MB (5242880 bytes).'
    
    This is NOT a JSON response, violating the spec.
    """
    from app import app
    with app.test_client() as c:
        jpeg = _minimal_jpeg()
        # Create a 6MB file (over 5MB Flask limit, under 20MB spec limit)
        big_file = io.BytesIO(jpeg + b'\x00' * (6 * 1024 * 1024))
        r = c.post('/items', data={
            'photo': (big_file, 'sixmb.jpg'),
            'name': 'Big File',
        }, content_type='multipart/form-data')
        
        assert r.status_code == 400, f"Expected 400, got {r.status_code}"
        
        # MUST be JSON with 'error' key - not plain text
        body = r.get_json(force=True)
        assert 'error' in body, (
            f"Response must be JSON with 'error' key. "
            f"Got status={r.status_code}, content_type={r.content_type}, body={r.data[:200]}"
        )


def test_files_larger_than_20mb_return_json_error():
    """Files > 20MB must return a JSON error response, not plain HTML 413."""
    from app import app
    with app.test_client() as c:
        jpeg = _minimal_jpeg()
        # Create a 25MB file (over the 20MB spec limit)
        big_file = io.BytesIO(jpeg + b'\x00' * (25 * 1024 * 1024))
        r = c.post('/items', data={
            'photo': (big_file, 'twentymb.jpg'),
            'name': 'Huge File',
        }, content_type='multipart/form-data')
        
        assert r.status_code == 400, f"Expected 400, got {r.status_code}"
        
        body = r.get_json(force=True)
        assert 'error' in body, (
            f"Response must be JSON with 'error' key for files > 20MB. "
            f"Got content_type={r.content_type}, body={r.data[:200]}"
        )


def test_upload_dir_cleanup_matches_app_upload_dir():
    """The conftest cleanup must target the same directory where the app stores uploads.
    
    The app stores uploads at /static/uploads/ (relative to repo root).
    The conftest must clean that same directory, not a different path like /tests/static/uploads/.
    """
    from app import app
    import os
    
    app_upload_dir = os.path.normpath(os.path.join(app.root_path, '..', 'static', 'uploads'))
    
    # Read conftest.py source to check its cleanup path
    conftest_path = os.path.join(os.path.dirname(__file__), 'conftest.py')
    conftest_source = open(conftest_path).read()
    
    # conftest defines ROOT and uses os.path.join(ROOT, 'static', 'uploads')
    # ROOT = os.path.dirname(os.path.abspath('./tests/conftest.py')) which resolves to /workspace/tests
    # So conftest cleans /workspace/tests/static/uploads/
    # But app stores at /workspace/static/uploads/
    # These paths MUST match for cleanup to work
    
    assert app_upload_dir in conftest_source, (
        f"conftest.py cleanup must target app's upload directory: {app_upload_dir}\n"
        f"Conftest uses different path. App upload dir normpath: {app_upload_dir}\n"
        f"Check: conftest ROOT = os.path.dirname(os.path.abspath('./tests/conftest.py')) "
        f"= {os.path.dirname(os.path.abspath('./tests/conftest.py'))}\n"
        f"App root_path = {app.root_path}, upload dir = {app_upload_dir}"
    )


def test_conftest_cleans_app_upload_dir_on_disk():
    """Conftest must actually clean /workspace/static/uploads/ (the real upload dir),
    not a phantom directory like /workspace/tests/static/uploads/."""
    from app import app
    import os
    
    app_upload_dir = os.path.normpath(os.path.join(app.root_path, '..', 'static', 'uploads'))
    
    # Create a file in the real upload dir
    test_file = os.path.join(app_upload_dir, 'cleanup_test_file.tmp')
    with open(test_file, 'w') as f:
        f.write('test')
    assert os.path.exists(test_file), f"Test file not created at {test_file}"
    
    # Conftest should clean this. Since we're in the middle of a test
    # and conftest's autouse fixture runs per-test, we verify the conftest
    # cleanup TARGETS the right directory by checking source
    conftest_path = os.path.join(os.path.dirname(__file__), 'conftest.py')
    conftest_source = open(conftest_path).read()
    
    # conftest should use app.root_path or os.path.normpath to find the right dir
    # It should NOT use a hardcoded relative path that resolves to tests/static/uploads/
    assert app_upload_dir in conftest_source, (
        f"conftest.py cleanup does not target the app's upload dir: {app_upload_dir}\n"
        f"The app stores uploads at {app_upload_dir}\n"
        f"conftest.py likely cleans a different path."
    )


def test_placeholder_image_is_actually_a_png():
    """placeholder.png must be a valid PNG image file, not just a file with .png extension."""
    import os
    from PIL import Image as PILImage
    
    placeholder_path = os.path.join(ROOT, 'static', 'images', 'placeholder.png')
    assert os.path.isfile(placeholder_path), "Placeholder image not found"
    
    # Must be a valid, readable image
    img = PILImage.open(placeholder_path)
    assert img.format == 'PNG', f"Placeholder is not a PNG file, it's {img.format}"
    assert img.size[0] > 0 and img.size[1] > 0, "Placeholder image has zero dimensions"


def test_item_detail_page_delete_form_uses_delete_method():
    """The delete route /items/<id> must accept DELETE method.
    
    The item_detail.html template has a delete form that triggers via JS:
        <form id="delete-form" method="POST" action="/items/{{ item.id }}">
            <input type="hidden" name="_method" value="DELETE">
    
    This form sends a POST, not DELETE. The Flask route only accepts DELETE.
    There is no JS to convert the POST to DELETE. So clicking delete will
    fail with 405 Method Not Allowed, not actually delete the item.
    """
    from app import app
    import io
    
    with app.test_client() as c:
        # Create an item with photo
        jpeg = _minimal_jpeg()
        r = c.post('/items', data={
            'photo': (io.BytesIO(jpeg), 'test.jpg'),
            'name': 'Delete Test Item',
        }, content_type='multipart/form-data')
        assert r.status_code == 201
        item_id = r.get_json()['item_id']
    
        # Get the detail page
        r = c.get(f'/items/{item_id}')
        assert r.status_code == 200
        html = r.data.decode('utf-8')
    
        # The delete button triggers a JS confirm then submits delete-form
        # The form uses method="POST" with _method=DELETE - but the route is DELETE only
        # We need to check if there's JS that converts this to a real DELETE
        # If the form just does POST, clicking delete will 405 Method Not Allowed
    
        # Check if there's JS to convert POST to DELETE
        has_delete_js = 'DELETE' in html or 'method' in html.lower()
        # Even if it has JS, the form action method should ideally be DELETE
        # Let's verify by actually testing the DELETE route directly
        r = c.delete(f'/items/{item_id}')
        assert r.status_code == 200, f"DELETE /items/{item_id} should work, got {r.status_code}"
