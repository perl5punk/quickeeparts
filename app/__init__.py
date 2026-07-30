from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['DATABASE'] = 'quickeeparts.db'
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB

from app import routes

if __name__ == '__main__':
    app.run(debug=True)
