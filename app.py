import sqlite3
import os
from flask import Flask, request, redirect, url_for, render_template, g

app = Flask(__name__)

DATABASE = os.path.join(app.instance_path, 'junk.db')


def get_db():
    """Open a new database connection if there is none yet for the
    current application context."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Close the database connection at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    """Initialize the database, creating the junk table if it doesn't exist."""
    with app.app_context():
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
        db.commit()


# Ensure the instance directory exists and the database is initialized.
os.makedirs(app.instance_path, exist_ok=True)
init_db()


@app.route('/')
def index():
    """Landing page with links to add and list junk items."""
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Display the add form (GET) or process a new junk submission (POST)."""
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
    """Display all junk items ordered by date_added descending."""
    db = get_db()
    items = db.execute(
        'SELECT id, name, description, category, date_added FROM junk ORDER BY date_added DESC'
    ).fetchall()
    return render_template('list.html', items=items)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
