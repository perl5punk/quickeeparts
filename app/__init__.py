from flask import Flask, render_template, redirect, url_for, g, request
from app.models import db
import os
import uuid

app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB

# Backward-compatible config for legacy app.py tests
UPLOAD_FOLDER = os.path.join(app.instance_path, 'photos')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DATABASE'] = os.path.join(app.instance_path, 'junk.db')
DATABASE = app.config['DATABASE']

# Ensure instance and upload directories exist
os.makedirs(app.instance_path, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def _init_legacy_db():
    """Create legacy junk table with photo_path for backward compatibility."""
    import sqlite3
    db_path = app.config['DATABASE']
    conn = sqlite3.connect(db_path)
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS junk (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                date_added DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        columns = [row[1] for row in conn.execute('PRAGMA table_info(junk)').fetchall()]
        if 'photo_path' not in columns:
            conn.execute('ALTER TABLE junk ADD COLUMN photo_path TEXT')
        conn.commit()
    finally:
        conn.close()


with app.app_context():
    _init_legacy_db()


# ─── Backward-compatible routes using the legacy junk table ───

LEGACY_ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
LEGACY_ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png'}


def _secure_filename(filename):
    """Generate a safe filename to prevent path traversal attacks."""
    if '..' in filename or '/' in filename or '\\' in filename:
        filename = os.path.basename(filename)
    ext = filename.rsplit('.', 1)[1] if '.' in filename else ''
    ext = ext.lower()
    return f'{uuid.uuid4()}.{ext}'


def _get_db():
    """Open a new database connection if there is none yet."""
    if 'db' not in g:
        import sqlite3
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def _close_db(exception):
    """Close the database connection at the end of the request."""
    db_conn = g.pop('db', None)
    if db_conn is not None:
        db_conn.close()


@app.route('/')
def index():
    """Landing page with links to /add and /list."""
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Handle GET (show form) and POST (save item) for adding junk."""
    if request.method == 'POST':
        name = request.form.get('name', '')
        description = request.form.get('description', '')
        category = request.form.get('category', '')
        photo_path = None

        file = request.files.get('photo')
        if file and file.filename != '':
            # Validate file extension
            ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
            if ext not in LEGACY_ALLOWED_EXTENSIONS:
                return f'Invalid file type: "{ext}". Allowed types: jpg, jpeg, png', 400
            # Validate MIME type
            if file.mimetype not in LEGACY_ALLOWED_MIME_TYPES:
                return f'Invalid MIME type: "{file.mimetype}". Allowed types: image/jpeg, image/png', 400
            # Save file securely
            safe_name = _secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], safe_name))
            photo_path = f'photos/{safe_name}'

        db_conn = _get_db()
        db_conn.execute(
            'INSERT INTO junk (name, description, category, photo_path) VALUES (?, ?, ?, ?)',
            (name, description, category, photo_path)
        )
        db_conn.commit()
        return redirect(url_for('add'))
    return render_template('add.html')


@app.route('/list')
def list_items_legacy():
    """Display all junk items from the database."""
    db_conn = _get_db()
    items = db_conn.execute(
        'SELECT id, name, description, category, date_added FROM junk ORDER BY date_added DESC'
    ).fetchall()
    return render_template('list.html', items=items)


from app import routes
