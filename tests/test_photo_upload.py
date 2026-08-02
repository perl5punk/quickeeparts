"""Tests for photo upload and display for junk items (acceptance criteria)."""
import os
import io
import pytest

sys_path = __import__('sys').path
sys_path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.abspath(__file__))


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
            0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,
            0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
            0x08, 0x02, 0x00, 0x00, 0x00, 0x90, 0x77, 0x53,
            0xDE,
            0x00, 0x00, 0x00, 0x0C, 0x49, 0x44, 0x41, 0x54,
            0x08, 0xD7, 0x63, 0xF8, 0xCF, 0xC0, 0x00, 0x00,
            0x00, 0x02, 0x00, 0x01, 0xE2, 0x21, 0xBC, 0x33,
            0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44,
            0xAE, 0x42, 0x60, 0x82,
        ]
    )


def _minimal_gif():
    """Return a minimal valid GIF image (1x1 pixel)."""
    return bytes(
        [
            0x47, 0x49, 0x46, 0x38, 0x39, 0x61,
            0x01, 0x00, 0x01, 0x00, 0x80, 0x00,
            0x00, 0xFF, 0x00, 0x00, 0xFF, 0xFF,
            0xFF, 0x00, 0x00, 0x00, 0x21, 0xF9,
            0x04, 0x01, 0x00, 0x00, 0x00, 0x00,
            0x2C, 0x00, 0x00, 0x00, 0x00, 0x01,
            0x00, 0x01, 0x00, 0x00, 0x02, 0x02,
            0x44, 0x01, 0x00, 0x3B,
        ]
    )


# ─── Acceptance Criterion: Blueprints are registered ─────────────────────────

def test_items_blueprint_is_registered():
    """The items blueprint must be registered so /items/* routes work."""
    from app import app
    registered = [bp for bp in app.blueprints]
    assert 'items' in registered, (
        f"Blueprint 'items' not registered. Registered blueprints: {registered}"
    )


def test_items_route_list_exists():
    """GET /items must return 200 (not 404)."""
    from app import app
    with app.test_client() as c:
        r = c.get('/items')
        assert r.status_code == 200, f"GET /items returned {r.status_code}, not 200"


def test_items_route_new_exists():
    """GET /items/new must return 200 (not 404)."""
    from app import app
    with app.test_client() as c:
        r = c.get('/items/new')
        assert r.status_code == 200, f"GET /items/new returned {r.status_code}, not 200"


# ─── Acceptance Criterion: JunkItem model has photo_filename column ────────────

def test_junk_item_has_photo_filename_column():
    """JunkItem model must have a photo_filename column."""
    from app.junk_item import JunkItem
    from app.models import db
    assert hasattr(JunkItem, 'photo_filename'), "JunkItem missing photo_filename attribute"


def test_photo_filename_column_is_nullable():
    """photo_filename column must be nullable (nullable=True)."""
    from app.junk_item import JunkItem
    col = JunkItem.__table__.columns['photo_filename']
    assert col.nullable is True, "photo_filename column is not nullable"


# ─── Acceptance Criterion: Upload via /items/new POST (create with photo) ──────

def test_create_item_with_jpeg_photo_returns_201():
    """Creating an item with a valid JPEG photo returns 201."""
    from app import app
    with app.test_client() as c:
        jpeg = _minimal_jpeg()
        data = {
            'photo': (io.BytesIO(jpeg), 'test.jpg'),
            'name': 'JPEG Item',
            'description': 'Test',
            'category': 'Test',
        }
        r = c.post('/items', data=data, content_type='multipart/form-data')
        assert r.status_code == 201, f"Expected 201, got {r.status_code}: {r.data[:200]}"


def test_create_item_with_png_photo_returns_201():
    """Creating an item with a valid PNG photo returns 201."""
    from app import app
    with app.test_client() as c:
        png = _minimal_png()
        data = {
            'photo': (io.BytesIO(png), 'test.png'),
            'name': 'PNG Item',
            'description': 'Test',
            'category': 'Test',
        }
        r = c.post('/items', data=data, content_type='multipart/form-data')
        assert r.status_code == 201, f"Expected 201, got {r.status_code}: {r.data[:200]}"


def test_create_item_with_gif_photo_returns_201():
    """Creating an item with a valid GIF photo returns 201."""
    from app import app
    with app.test_client() as c:
        gif = _minimal_gif()
        data = {
            'photo': (io.BytesIO(gif), 'test.gif'),
            'name': 'GIF Item',
            'description': 'Test',
            'category': 'Test',
        }
        r = c.post('/items', data=data, content_type='multipart/form-data')
        assert r.status_code == 201, f"Expected 201, got {r.status_code}: {r.data[:200]}"


def test_create_item_without_photo_returns_201():
    """Creating an item without a photo still returns 201 (photo is optional)."""
    from app import app
    with app.test_client() as c:
        r = c.post('/items', data={
            'name': 'No Photo Item',
            'description': 'No photo',
            'category': 'Test',
        })
        assert r.status_code == 201, f"Expected 201, got {r.status_code}: {r.data[:200]}"


# ─── Acceptance Criterion: Upload rejects files > 20MB and wrong MIME types ────

def test_create_item_rejects_non_image_mime_type():
    """Uploading a file with invalid MIME type returns JSON 400 error."""
    from app import app
    with app.test_client() as c:
        data = {
            'photo': (io.BytesIO(b'this is not an image'), 'test.jpg'),
            'name': 'Bad Mime',
            'description': 'Test',
        }
        r = c.post('/items', data=data, content_type='multipart/form-data')
        assert r.status_code == 400, f"Expected 400, got {r.status_code}: {r.data[:200]}"
        body = r.get_json(force=True)
        assert 'error' in body, f"Expected JSON error response, got: {r.data[:200]}"


def test_create_item_rejects_text_file():
    """Uploading a .txt file returns JSON 400 error."""
    from app import app
    with app.test_client() as c:
        data = {
            'photo': (io.BytesIO(b'text content'), 'test.txt'),
            'name': 'Bad File',
            'description': 'Test',
        }
        r = c.post('/items', data=data, content_type='multipart/form-data')
        assert r.status_code == 400, f"Expected 400, got {r.status_code}: {r.data[:200]}"
        body = r.get_json(force=True)
        assert 'error' in body


def test_create_item_name_required():
    """Creating an item without a name returns JSON 400 error."""
    from app import app
    with app.test_client() as c:
        r = c.post('/items', data={
            'description': 'No name',
            'category': 'Test',
        })
        assert r.status_code == 400, f"Expected 400, got {r.status_code}: {r.data[:200]}"
        body = r.get_json(force=True)
        assert 'error' in body


# ─── Acceptance Criterion: Image resized on upload, original not kept ─────────

def test_image_is_resized_on_upload():
    """After upload, the stored image is resized (not the original 1x1 JPEG bytes)."""
    from app import app
    import os
    from PIL import Image as PILImage
    with app.test_client() as c:
        img = PILImage.new('RGB', (1500, 1000), color='red')
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        buf.seek(0)
        data = {
            'photo': (buf, 'large.jpg'),
            'name': 'Resized Item',
            'description': 'Should be resized',
            'category': 'Test',
        }
        r = c.post('/items', data=data, content_type='multipart/form-data')
        assert r.status_code == 201, f"Upload failed: {r.data[:200]}"
        resp = r.get_json()
        photo_filename = resp['photo_filename']
        assert photo_filename is not None, "photo_filename should be set"
        upload_dir = os.path.join(app.root_path, '..', 'static', 'uploads')
        full_path = os.path.join(upload_dir, photo_filename)
        assert os.path.exists(full_path), f"Uploaded file not found at {full_path}"
        img2 = PILImage.open(full_path)
        w, h = img2.size
        assert max(w, h) <= 1200, (
            f"Image not resized. Longest side {max(w, h)} > 1200px (got {w}x{h})"
        )


def test_original_file_not_kept():
    """The uploaded original file is not stored; only the resized version."""
    from app import app
    with app.test_client() as c:
        jpeg = _minimal_jpeg()
        data = {
            'photo': (io.BytesIO(jpeg), 'test.jpg'),
            'name': 'No Original',
            'description': 'Test',
        }
        r = c.post('/items', data=data, content_type='multipart/form-data')
        assert r.status_code == 201
        resp = r.get_json()
        photo_filename = resp['photo_filename']
        assert photo_filename != 'test.jpg', (
            f"Original filename '{photo_filename}' was stored instead of unique name"
        )


# ─── Acceptance Criterion: Thumbnail generated ────────────────────────────────

def test_thumbnail_is_generated():
    """A thumbnail image is generated and stored in /static/uploads/thumbnails/."""
    from app import app
    import os
    with app.test_client() as c:
        jpeg = _minimal_jpeg()
        data = {
            'photo': (io.BytesIO(jpeg), 'thumb_test.jpg'),
            'name': 'Thumbnail Item',
            'description': 'Test',
        }
        r = c.post('/items', data=data, content_type='multipart/form-data')
        assert r.status_code == 201
        resp = r.get_json()
        photo_filename = resp['photo_filename']
        upload_dir = os.path.join(app.root_path, '..', 'static', 'uploads')
        thumb_path = os.path.join(
            upload_dir, 'thumbnails',
            f'{photo_filename.rsplit(".", 1)[0]}_thumb.jpg'
        )
        assert os.path.exists(thumb_path), f"Thumbnail not found at {thumb_path}"


def test_thumbnail_max_200x200():
    """Thumbnail is scaled to fit within 200x200px."""
    from app import app
    import os
    from PIL import Image as PILImage
    with app.test_client() as c:
        img = PILImage.new('RGB', (1500, 1000), color='blue')
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        buf.seek(0)
        data = {
            'photo': (buf, 'big.jpg'),
            'name': 'Big Thumbnail Item',
            'description': 'Test',
        }
        r = c.post('/items', data=data, content_type='multipart/form-data')
        assert r.status_code == 201
        resp = r.get_json()
        photo_filename = resp['photo_filename']
        upload_dir = os.path.join(app.root_path, '..', 'static', 'uploads')
        thumb_path = os.path.join(
            upload_dir, 'thumbnails',
            f'{photo_filename.rsplit(".", 1)[0]}_thumb.jpg'
        )
        thumb_img = PILImage.open(thumb_path)
        w, h = thumb_img.size
        assert w <= 200 and h <= 200, f"Thumbnail exceeds 200x200: {w}x{h}"


# ─── Acceptance Criterion: Files stored in /static/uploads/ ───────────────────

def test_photo_stored_in_static_uploads():
    """Uploaded image is stored in /static/uploads/ directory."""
    from app import app
    import os
    with app.test_client() as c:
        jpeg = _minimal_jpeg()
        data = {
            'photo': (io.BytesIO(jpeg), 'store_test.jpg'),
            'name': 'Store Test',
            'description': 'Test',
        }
        r = c.post('/items', data=data, content_type='multipart/form-data')
        assert r.status_code == 201
        resp = r.get_json()
        photo_filename = resp['photo_filename']
        upload_dir = os.path.join(app.root_path, '..', 'static', 'uploads')
        full_path = os.path.join(upload_dir, photo_filename)
        assert os.path.exists(full_path), f"File not at {full_path}"


def test_filename_format():
    """Filename follows {item_id}_{timestamp}.{ext} format."""
    from app import app
    with app.test_client() as c:
        jpeg = _minimal_jpeg()
        data = {
            'photo': (io.BytesIO(jpeg), 'anything.jpg'),
            'name': 'Filename Test',
            'description': 'Test',
        }
        r = c.post('/items', data=data, content_type='multipart/form-data')
        assert r.status_code == 201
        resp = r.get_json()
        photo_filename = resp['photo_filename']
        assert photo_filename.startswith('1_'), (
            f"Filename should start with item ID: {photo_filename}"
        )
        assert photo_filename.endswith('.jpg'), (
            f"Filename should end with .jpg: {photo_filename}"
        )


# ─── Acceptance Criterion: Listing page displays thumbnails ───────────────────

def test_listing_page_displays_thumbnail_for_photo_item():
    """GET /items shows a thumbnail for items that have photos."""
    from app import app
    with app.test_client() as c:
        jpeg = _minimal_jpeg()
        data = {
            'photo': (io.BytesIO(jpeg), 'list_photo.jpg'),
            'name': 'List Item With Photo',
            'description': 'For listing test',
        }
        c.post('/items', data=data, content_type='multipart/form-data')
        r = c.get('/items')
        assert r.status_code == 200
        html = r.data.decode('utf-8')
        assert 'List Item With Photo' in html
        assert 'thumb.jpg' in html or 'thumbnail' in html.lower(), (
            f"Thumbnail not found in listing HTML: {html[:500]}"
        )


def test_listing_page_shows_placeholder_for_no_photo():
    """GET /items shows placeholder for items without photos."""
    from app import app
    with app.test_client() as c:
        c.post('/items', data={
            'name': 'No Photo Item',
            'description': 'No photo',
        })
        r = c.get('/items')
        assert r.status_code == 200
        html = r.data.decode('utf-8')
        assert 'No Photo Item' in html
        assert 'placeholder' in html.lower(), (
            f"Placeholder not shown for item without photo: {html[:500]}"
        )


# ─── Acceptance Criterion: Detail page displays full-size image ──────────────

def test_detail_page_displays_full_image():
    """GET /items/<id> shows full-size image for item with photo."""
    from app import app
    with app.test_client() as c:
        jpeg = _minimal_jpeg()
        data = {
            'photo': (io.BytesIO(jpeg), 'detail.jpg'),
            'name': 'Detail Item',
            'description': 'Detail test',
        }
        r = c.post('/items', data=data, content_type='multipart/form-data')
        assert r.status_code == 201
        item_id = r.get_json()['item_id']
        r = c.get(f'/items/{item_id}')
        assert r.status_code == 200
        html = r.data.decode('utf-8')
        assert 'Detail Item' in html
        assert 'uploads' in html and '.jpg' in html, (
            f"Full-size image not found in detail page HTML"
        )


def test_detail_page_placeholder_for_no_photo():
    """GET /items/<id> shows placeholder for item without photo."""
    from app import app
    with app.test_client() as c:
        c.post('/items', data={
            'name': 'Detail No Photo',
            'description': 'No photo',
        })
        r = c.get('/items/1')
        assert r.status_code == 200
        html = r.data.decode('utf-8')
        assert 'placeholder' in html.lower(), (
            f"Placeholder not shown: {html[:500]}"
        )


# ─── Acceptance Criterion: Thumbnail serving route ────────────────────────────

def test_thumbnail_serving_route_exists():
    """GET /static/uploads/thumbnails/<filename> serves thumbnails."""
    from app import app
    with app.test_client() as c:
        jpeg = _minimal_jpeg()
        data = {
            'photo': (io.BytesIO(jpeg), 'serve_thumb.jpg'),
            'name': 'Serve Thumbnail',
            'description': 'Test',
        }
        c.post('/items', data=data, content_type='multipart/form-data')
        from app.junk_item import JunkItem
        item = JunkItem.query.first()
        thumb_path = f"{item.photo_filename.rsplit('.', 1)[0]}_thumb.jpg"
        r = c.get(f'/static/uploads/thumbnails/{thumb_path}')
        assert r.status_code == 200, (
            f"Thumbnail serving route returned {r.status_code}, expected 200"
        )


def test_full_image_serving_route_exists():
    """GET /static/uploads/<filename> serves full-size images."""
    from app import app
    with app.test_client() as c:
        jpeg = _minimal_jpeg()
        data = {
            'photo': (io.BytesIO(jpeg), 'serve_full.jpg'),
            'name': 'Serve Full',
            'description': 'Test',
        }
        c.post('/items', data=data, content_type='multipart/form-data')
        from app.junk_item import JunkItem
        item = JunkItem.query.first()
        r = c.get(f'/static/uploads/{item.photo_filename}')
        assert r.status_code == 200, (
            f"Full image serving route returned {r.status_code}, expected 200"
        )


# ─── Acceptance Criterion: Placeholder image exists ──────────────────────────

def test_placeholder_image_exists():
    """A placeholder image exists at /static/images/placeholder.png."""
    assert os.path.isfile(os.path.join(ROOT, 'static', 'images', 'placeholder.png')), (
        "Placeholder image not found at /static/images/placeholder.png"
    )


def test_placeholder_served_by_route():
    """GET /static/images/placeholder.png returns the placeholder image."""
    from app import app
    with app.test_client() as c:
        r = c.get('/static/images/placeholder.png')
        assert r.status_code == 200, (
            f"Placeholder route returned {r.status_code}"
        )


# ─── Acceptance Criterion: Delete item removes photo files from disk ──────────

def test_delete_item_removes_photo_files():
    """Deleting a junk item removes its full-size and thumbnail images from disk."""
    from app import app
    import os
    with app.test_client() as c:
        jpeg = _minimal_jpeg()
        data = {
            'photo': (io.BytesIO(jpeg), 'delete_photo.jpg'),
            'name': 'Delete Photo Item',
            'description': 'Should be deleted',
        }
        r = c.post('/items', data=data, content_type='multipart/form-data')
        assert r.status_code == 201
        item_id = r.get_json()['item_id']
        from app.junk_item import JunkItem
        item = JunkItem.query.get(item_id)
        upload_dir = os.path.join(app.root_path, '..', 'static', 'uploads')
        full_path = os.path.join(upload_dir, item.photo_filename)
        thumb_path = os.path.join(
            upload_dir, 'thumbnails',
            f'{item.photo_filename.rsplit(".", 1)[0]}_thumb.jpg'
        )
        assert os.path.exists(full_path), "Full-size image should exist before delete"
        assert os.path.exists(thumb_path), "Thumbnail should exist before delete"
        r = c.delete(f'/items/{item_id}')
        assert r.status_code == 200
        assert not os.path.exists(full_path), f"Full-size image not deleted: {full_path}"
        assert not os.path.exists(thumb_path), f"Thumbnail not deleted: {thumb_path}"


# ─── Acceptance Criterion: Edit item replaces photo ──────────────────────────

def test_edit_item_replaces_photo():
    """Editing an item with a new photo replaces the old photo files."""
    from app import app
    import os
    with app.test_client() as c:
        jpeg1 = _minimal_jpeg()
        r1 = c.post('/items', data={
            'photo': (io.BytesIO(jpeg1), 'old_photo.jpg'),
            'name': 'Edit Test',
            'description': 'Old photo',
        }, content_type='multipart/form-data')
        assert r1.status_code == 201
        item_id = r1.get_json()['item_id']
        from app.junk_item import JunkItem
        item = JunkItem.query.get(item_id)
        upload_dir = os.path.join(app.root_path, '..', 'static', 'uploads')
        old_photo_path = os.path.join(upload_dir, item.photo_filename)
        assert os.path.exists(old_photo_path)

        jpeg2 = _minimal_png()
        r2 = c.put(f'/items/{item_id}', data={
            'name': 'Edit Test',
            'photo': (io.BytesIO(jpeg2), 'new_photo.png'),
        }, content_type='multipart/form-data')
        assert r2.status_code == 200, f"PUT /items/{item_id} returned {r2.status_code}: {r2.data[:200]}"

        item = JunkItem.query.get(item_id)
        new_photo_path = os.path.join(upload_dir, item.photo_filename)
        assert not os.path.exists(old_photo_path), "Old photo should be deleted"
        assert os.path.exists(new_photo_path), "New photo should exist"


def test_edit_item_photo_replacement_old_thumb_gone():
    """When editing with a new photo, the old thumbnail is also deleted."""
    from app import app
    import os
    with app.test_client() as c:
        jpeg1 = _minimal_jpeg()
        r1 = c.post('/items', data={
            'photo': (io.BytesIO(jpeg1), 'thumb_old.jpg'),
            'name': 'Thumb Edit',
            'description': 'Test',
        }, content_type='multipart/form-data')
        assert r1.status_code == 201
        item_id = r1.get_json()['item_id']
        from app.junk_item import JunkItem
        item = JunkItem.query.get(item_id)
        upload_dir = os.path.join(app.root_path, '..', 'static', 'uploads')
        old_thumb = os.path.join(
            upload_dir, 'thumbnails',
            f'{item.photo_filename.rsplit(".", 1)[0]}_thumb.jpg'
        )
        assert os.path.exists(old_thumb)

        jpeg2 = _minimal_png()
        r2 = c.put(f'/items/{item_id}', data={
            'name': 'Thumb Edit',
            'photo': (io.BytesIO(jpeg2), 'thumb_new.png'),
        }, content_type='multipart/form-data')
        assert r2.status_code == 200

        item = JunkItem.query.get(item_id)
        new_thumb = os.path.join(
            upload_dir, 'thumbnails',
            f'{item.photo_filename.rsplit(".", 1)[0]}_thumb.jpg'
        )
        assert not os.path.exists(old_thumb), "Old thumbnail should be deleted"
        assert os.path.exists(new_thumb), "New thumbnail should exist"


# ─── Acceptance Criterion: JSON error response on validation failure ──────────

def test_validation_error_is_json():
    """Validation errors return JSON (not plain text) responses."""
    from app import app
    with app.test_client() as c:
        r = c.post('/items', data={
            'photo': (io.BytesIO(b'not image'), 'test.txt'),
            'name': 'Bad',
        }, content_type='multipart/form-data')
        assert r.status_code == 400
        data = r.get_json(force=True)
        assert isinstance(data, dict), f"Response should be JSON object, got {type(data)}"
        assert 'error' in data, f"JSON response missing 'error' key: {data}"


def test_validation_error_contains_error_message():
    """JSON error response includes a descriptive error message."""
    from app import app
    with app.test_client() as c:
        r = c.post('/items', data={
            'photo': (io.BytesIO(b'not image'), 'test.bmp'),
            'name': 'Bad Type',
        }, content_type='multipart/form-data')
        assert r.status_code == 400
        data = r.get_json(force=True)
        assert isinstance(data['error'], str) and len(data['error']) > 0, (
            f"Error message should be non-empty string: {data}"
        )


# ─── Acceptance Criterion: Create form has file input ────────────────────────

def test_create_form_has_file_input():
    """The create item form includes a file input with name='photo'."""
    from app import app
    with app.test_client() as c:
        r = c.get('/items/new')
        assert r.status_code == 200
        html = r.data.decode('utf-8')
        assert 'type="file"' in html, "Form missing file input"
        assert 'name="photo"' in html or "name='photo'" in html, "File input missing name='photo'"


def test_create_form_has_label():
    """The create form has a label for photo upload."""
    from app import app
    with app.test_client() as c:
        r = c.get('/items/new')
        html = r.data.decode('utf-8')
        assert 'Upload Photo' in html or 'photo' in html.lower(), (
            "Create form missing photo upload label"
        )


def test_create_form_has_file_type_hint():
    """The create form shows hint about accepted formats."""
    from app import app
    with app.test_client() as c:
        r = c.get('/items/new')
        html = r.data.decode('utf-8')
        assert 'JPG' in html or 'jpg' in html, "Missing JPG hint"
        assert 'PNG' in html or 'png' in html, "Missing PNG hint"
        assert 'GIF' in html or 'gif' in html, "Missing GIF hint"
        assert '20MB' in html or '20' in html, "Missing max size hint"


def test_create_form_has_client_side_validation():
    """The create form includes client-side validation for file type."""
    from app import app
    with app.test_client() as c:
        r = c.get('/items/new')
        html = r.data.decode('utf-8')
        assert 'script' in html.lower(), "Create form missing client-side script"
        assert 'invalid file type' in html.lower() or 'valid' in html.lower(), (
            "Create form missing client-side file type validation"
        )


# ─── Acceptance Criterion: Edit form has file input ──────────────────────────

def test_edit_form_has_file_input():
    """The edit item form includes a file input with name='photo'."""
    from app import app
    with app.test_client() as c:
        jpeg = _minimal_jpeg()
        r1 = c.post('/items', data={
            'photo': (io.BytesIO(jpeg), 'edit_photo.jpg'),
            'name': 'Edit Form Item',
        }, content_type='multipart/form-data')
        assert r1.status_code == 201
        item_id = r1.get_json()['item_id']
        r2 = c.get(f'/items/{item_id}/edit')
        assert r2.status_code == 200
        html = r2.data.decode('utf-8')
        assert 'type="file"' in html, "Edit form missing file input"
        assert 'name="photo"' in html or "name='photo'" in html, "Edit form missing name='photo'"


def test_edit_form_has_client_side_validation():
    """The edit form includes client-side validation for file type."""
    from app import app
    with app.test_client() as c:
        jpeg = _minimal_jpeg()
        r1 = c.post('/items', data={
            'photo': (io.BytesIO(jpeg), 'edit_client.jpg'),
            'name': 'Edit Client Test',
        }, content_type='multipart/form-data')
        assert r1.status_code == 201
        item_id = r1.get_json()['item_id']
        r2 = c.get(f'/items/{item_id}/edit')
        html = r2.data.decode('utf-8')
        assert 'script' in html.lower(), "Edit form missing client-side script"
        assert 'invalid file type' in html.lower() or 'valid' in html.lower(), (
            "Edit form missing client-side file type validation"
        )


# ─── Acceptance Criterion: MIME type validation accepts jpg, png, gif ─────────

def test_mime_type_jpg_accepted():
    """Valid JPEG file is accepted."""
    from app import app
    with app.test_client() as c:
        r = c.post('/items', data={
            'photo': (io.BytesIO(_minimal_jpeg()), 'valid.jpg'),
            'name': 'JPG Valid',
        }, content_type='multipart/form-data')
        assert r.status_code == 201, f"JPEG accepted but got {r.status_code}: {r.data[:200]}"


def test_mime_type_png_accepted():
    """Valid PNG file is accepted."""
    from app import app
    with app.test_client() as c:
        r = c.post('/items', data={
            'photo': (io.BytesIO(_minimal_png()), 'valid.png'),
            'name': 'PNG Valid',
        }, content_type='multipart/form-data')
        assert r.status_code == 201, f"PNG accepted but got {r.status_code}: {r.data[:200]}"


def test_mime_type_gif_accepted():
    """Valid GIF file is accepted."""
    from app import app
    with app.test_client() as c:
        r = c.post('/items', data={
            'photo': (io.BytesIO(_minimal_gif()), 'valid.gif'),
            'name': 'GIF Valid',
        }, content_type='multipart/form-data')
        assert r.status_code == 201, f"GIF accepted but got {r.status_code}: {r.data[:200]}"
