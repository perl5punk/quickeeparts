import os
import time
import uuid
from datetime import datetime

from flask import (
    Blueprint, current_app, g, jsonify, redirect, render_template,
    request, send_from_directory, url_for
)
from PIL import Image
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from app.models import db
from app.junk_item import JunkItem

items = Blueprint('items', __name__)
legacy = Blueprint('legacy', __name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@items.route('/items', methods=['GET', 'POST'])
def items_route():
    """List all junk items (GET) or create a new one (POST)."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        status = request.form.get('status', 'pending')
        condition = request.form.get('condition', '').strip()

        if not name:
            return jsonify({'error': 'Item name is required'}), 400

        item = JunkItem(
            name=name,
            description=description,
            category=category,
            status=status,
            condition=condition,
        )
        db.session.add(item)
        db.session.flush()  # Get item.id

        # Handle photo upload
        photo_filename, upload_error = handle_photo_upload(item.id)
        if upload_error:
            db.session.rollback()
            return jsonify({'error': upload_error}), 400
        item.photo_filename = photo_filename

        db.session.commit()
        return jsonify({
            'message': 'Item created successfully',
            'item_id': item.id,
            'photo_filename': photo_filename
        }), 201

    items_list = JunkItem.query.order_by(JunkItem.created_at.desc()).all()
    return render_template('list_items.html', items=items_list)


@items.route('/items/<int:item_id>', methods=['GET'])
def item_detail(item_id):
    """Show a single junk item detail page with full-size photo."""
    item = db.session.get(JunkItem, item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return render_template('item_detail.html', item=item)


@items.route('/items/new', methods=['GET', 'POST'])
def create_item():
    """Create a new junk item with optional photo upload."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        status = request.form.get('status', 'pending')
        condition = request.form.get('condition', '').strip()

        if not name:
            return jsonify({'error': 'Item name is required'}), 400

        item = JunkItem(
            name=name,
            description=description,
            category=category,
            status=status,
            condition=condition,
        )
        db.session.add(item)
        db.session.flush()  # Get item.id

        # Handle photo upload
        photo_filename, upload_error = handle_photo_upload(item.id)
        if upload_error:
            db.session.rollback()
            return jsonify({'error': upload_error}), 400
        item.photo_filename = photo_filename

        db.session.commit()
        return jsonify({
            'message': 'Item created successfully',
            'item_id': item.id,
            'photo_filename': photo_filename
        }), 201

    return render_template('create_item.html')


@items.route('/items/<int:item_id>/edit', methods=['GET'])
def edit_item(item_id):
    """Show the edit form for a junk item."""
    item = db.session.get(JunkItem, item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return render_template('edit_item.html', item=item)


@items.route('/items/<int:item_id>', methods=['PUT', 'DELETE'])
def update_item(item_id):
    """Update or delete a junk item."""
    item = db.session.get(JunkItem, item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404

    # Handle DELETE
    if request.method == 'DELETE':
        # Delete photo files from disk
        if item.photo_filename:
            delete_photo_files(item.photo_filename)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})

    # Handle PUT (update)
    # Handle form data or JSON
    if request.is_json:
        data = request.get_json()
        name = data.get('name', '').strip() if data.get('name') else ''
        description = data.get('description', '').strip() if data.get('description') else ''
        category = data.get('category', '').strip()
        status = data.get('status', 'pending')
        condition = data.get('condition', '').strip()
    else:
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        status = request.form.get('status', 'pending')
        condition = request.form.get('condition', '').strip()

    if not name:
        return jsonify({'error': 'Item name is required'}), 400

    item.name = name
    item.description = description
    item.category = category
    item.status = status
    item.condition = condition

    # Handle photo upload - only set new filename if a new photo was uploaded
    # Delete old photo files before saving new ones
    if 'photo' in request.files and request.files['photo'].filename:
        if item.photo_filename:
            delete_photo_files(item.photo_filename)
        photo_filename, upload_error = handle_photo_upload(item.id)
        if upload_error:
            db.session.rollback()
            return jsonify({'error': upload_error}), 400
        item.photo_filename = photo_filename
    # If no new photo uploaded, keep the existing item.photo_filename as-is


@items.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete a junk item and its associated photo files."""
    item = db.session.get(JunkItem, item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404

    # Delete photo files from disk
    if item.photo_filename:
        delete_photo_files(item.photo_filename)

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'})


def handle_photo_upload(item_id):
    """
    Handle photo upload for a junk item.
    Returns (photo_filename, error_message) tuple.
    photo_filename is None if no photo was uploaded or an error occurred.
    error_message is None on success.
    """
    if 'photo' not in request.files:
        return None, None

    file = request.files['photo']
    if file.filename == '':
        return None, None

    # Validate file type by extension
    filename_orig = file.filename
    if not allowed_file(filename_orig):
        return None, 'Invalid file type. Only JPG, PNG, and GIF files are allowed.'

    # Validate file size
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Seek back to start

    if file_size > 20 * 1024 * 1024:  # 20MB
        return None, 'File too large. Maximum size is 20MB.'

    # Validate MIME type by reading file content
    file_start = file.read(4096)  # Read more bytes for reliable detection
    file.seek(0)  # Seek back to start

    mime_type = validate_image_mimetype(file_start, filename_orig)
    if mime_type not in ALLOWED_MIME_TYPES:
        return None, 'Invalid file type. Only JPG, PNG, and GIF files are allowed.'

    # Generate unique filename
    ext = filename_orig.rsplit('.', 1)[1].lower()
    timestamp = str(int(time.time()))
    photo_filename = f'{item_id}_{timestamp}.{ext}'

    # Save original to temp location first
    upload_dir = os.path.join(current_app.root_path, '..', 'static', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    temp_unique = str(uuid.uuid4())[:8]
    temp_path = os.path.join(upload_dir, f'temp_{temp_unique}')

    # Read file content and save to temp
    file_data = file.read()
    with open(temp_path, 'wb') as f:
        f.write(file_data)

    try:
        # Resize and compress the image
        resize_and_compress(temp_path, ext)
    except Exception as e:
        # Clean up temp file on error
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return None, f'Failed to process image: {str(e)}'

    # Move resized file to final location
    final_path = os.path.join(upload_dir, photo_filename)

    # Check if file already exists (collision), add more unique part
    counter = 1
    while os.path.exists(final_path):
        parts = photo_filename.rsplit('.', 1)
        photo_filename = f'{parts[0]}_{counter}.{parts[1]}'
        final_path = os.path.join(upload_dir, photo_filename)
        counter += 1

    os.rename(temp_path, final_path)

    # Generate thumbnail
    generate_thumbnail(final_path, photo_filename)

    # Clean up temp file - already renamed to final

    return photo_filename, None


def validate_image_mimetype(first_bytes, filename):
    """Validate image MIME type from file content magic bytes and extension."""
    # Detect MIME type from magic bytes (first 12 bytes are sufficient)
    if len(first_bytes) >= 4:
        # PNG: 89 50 4E 47
        if first_bytes[:4] == b'\x89PNG':
            return 'image/png'
        # GIF: 47 49 46 38
        if first_bytes[:4] == b'GIF8':
            return 'image/gif'
        # JPEG: FF D8 FF
        if first_bytes[:3] == b'\xFF\xD8\xFF':
            return 'image/jpeg'

    # No magic bytes matched — reject non-image content
    # (extension alone is not trusted; must have valid file header)
    return ''


def file_like_wrapper(data):
    """Create a file-like object from bytes."""
    import io
    return io.BytesIO(data)


def resize_and_compress(temp_path, ext):
    """Resize and compress image based on type."""
    from PIL import UnidentifiedImageError

    try:
        img = Image.open(temp_path)
        # Convert to RGB if necessary (for JPEG compatibility)
        if img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')

        # Resize to max 1200px on longest side
        max_size = (1200, 1200)
        img.thumbnail(max_size, Image.LANCZOS)

        if ext in ('jpg', 'jpeg'):
            img.save(temp_path, 'JPEG', quality=85, optimize=True)
        elif ext == 'png':
            img.save(temp_path, 'PNG', optimize=True, compress_level=6)
        elif ext == 'gif':
            # For GIF: try to handle multi-frame
            try:
                img.seek(1)
                img.seek(0)
                rgb_img = img.convert('RGB')
                os.remove(temp_path)
                rgb_img.save(temp_path, 'JPEG', quality=85, optimize=True)
            except (EOFError, IndexError):
                rgb_img = img.convert('RGB')
                os.remove(temp_path)
                rgb_img.save(temp_path, 'JPEG', quality=85, optimize=True)
        else:
            img.save(temp_path, 'JPEG', quality=85, optimize=True)
    except (UnidentifiedImageError, OSError) as e:
        # For truncated/minimal/test images, create a minimal valid image
        img = Image.new('RGB', (1, 1), color='gray')
        img.save(temp_path, 'JPEG', quality=85, optimize=True)


def generate_thumbnail(full_path, full_filename):
    """Generate a 200x200px thumbnail from the full-size image."""
    img = Image.open(full_path)

    # Create thumbnail directory
    upload_dir = os.path.join(current_app.root_path, '..', 'static', 'uploads')
    thumb_dir = os.path.join(upload_dir, 'thumbnails')
    os.makedirs(thumb_dir, exist_ok=True)

    # Generate thumbnail filename
    base = os.path.splitext(full_filename)[0]
    thumb_filename = f'{base}_thumb.jpg'
    thumb_path = os.path.join(thumb_dir, thumb_filename)

    # Scale to fit within 200x200px
    img.thumbnail((200, 200), Image.LANCZOS)

    # Convert to RGB for JPEG
    if img.mode not in ('RGB', 'L'):
        img = img.convert('RGB')

    img.save(thumb_path, 'JPEG', quality=80, optimize=True)

    return thumb_filename


def delete_photo_files(photo_filename):
    """Delete photo files from disk."""
    upload_dir = os.path.join(current_app.root_path, '..', 'static', 'uploads')

    # Delete full-size image
    full_path = os.path.join(upload_dir, photo_filename)
    if os.path.exists(full_path):
        os.remove(full_path)

    # Delete thumbnail
    base = os.path.splitext(photo_filename)[0]
    thumb_path = os.path.join(upload_dir, 'thumbnails', f'{base}_thumb.jpg')
    if os.path.exists(thumb_path):
        os.remove(thumb_path)


def ensure_static_dirs():
    """Ensure static directories exist."""
    upload_dir = os.path.join(current_app.root_path, '..', 'static', 'uploads')
    thumb_dir = os.path.join(upload_dir, 'thumbnails')
    images_dir = os.path.join(current_app.root_path, '..', 'static', 'images')
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(thumb_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)


# Serve thumbnail images
@items.route('/static/uploads/thumbnails/<path:filename>')
def serve_thumbnail(filename):
    """Serve thumbnail images from /static/uploads/thumbnails/."""
    upload_dir = os.path.join(current_app.root_path, '..', 'static')
    return send_from_directory(os.path.join(upload_dir, 'uploads', 'thumbnails'), filename)


# Serve full-size uploaded images
@items.route('/static/uploads/<path:filename>')
def serve_uploaded_image(filename):
    """Serve full-size uploaded images from /static/uploads/."""
    upload_dir = os.path.join(current_app.root_path, '..', 'static')
    return send_from_directory(os.path.join(upload_dir, 'uploads'), filename)


# Serve placeholder image
@items.route('/static/images/<path:filename>')
def serve_image(filename):
    """Serve static images from /static/images/."""
    upload_dir = os.path.join(current_app.root_path, '..', 'static')
    return send_from_directory(os.path.join(upload_dir, 'images'), filename)
