from flask import Flask, render_template, redirect, url_for, g
from app.models import db
import os

app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB

# Backward-compatible config for legacy app.py tests
UPLOAD_FOLDER = os.path.join(app.instance_path, 'photos')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DATABASE'] = os.path.join(app.instance_path, 'junk.db')
DATABASE = app.config['DATABASE']

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png'}

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

from app import routes

if __name__ == '__main__':
    app.run(debug=True)
