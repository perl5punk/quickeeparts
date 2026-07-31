import os
import sqlite3
import uuid
from flask import Flask, render_template, request, redirect, url_for, g, flash

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'dev-key'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB
UPLOAD_FOLDER = os.path.join(app.instance_path, 'photos')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure instance and upload directories exist
os.makedirs(app.instance_path, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DATABASE = os.path.join(app.instance_path, 'junk.db')

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png'}


def secure_filename(filename):
    """Generate a safe filename to prevent path traversal attacks."""
    if '..' in filename or '/' in filename or '\\' in filename:
        filename = os.path.basename(filename)
    ext = filename.rsplit('.', 1)[1] if '.' in filename else ''
    ext = ext.lower()
    return f'{uuid.uuid4()}.{ext}'


def get_db():
    """Open a new database connection if there is none yet for the current app context."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    """Close the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """Create the junk table if it does not exist, and migrate for photo_path."""
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS junk (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Migrate: add photo_path column if it does not exist
    columns = [row[1] for row in db.execute('PRAGMA table_info(junk)').fetchall()]
    if 'photo_path' not in columns:
        db.execute('ALTER TABLE junk ADD COLUMN photo_path TEXT')
    db.commit()


# Initialize the database at app startup
with app.app_context():
    init_db()


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
        db = get_db()
        db.execute(
            'INSERT INTO junk (name, description, category) VALUES (?, ?, ?)',
            (name, description, category)
        )
        db.commit()
        return redirect(url_for('add'))
    return render_template('add.html')


@app.route('/list')
def list():
    """Display all junk items from the database."""
    db = get_db()
    items = db.execute(
        'SELECT id, name, description, category, date_added FROM junk ORDER BY date_added DESC'
    ).fetchall()
    return render_template('list.html', items=items)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
