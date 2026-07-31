from app import create_app, db


def test_create_app_returns_app():
    """Test that create_app returns a configured Flask app with proper defaults."""
    app = create_app()
    assert app is not None
    assert app.config['SECRET_KEY'] is not None
    assert app.config['SQLALCHEMY_DATABASE_URI'] == f'sqlite:///{app.instance_path}/app.db'
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False


def test_home_route():
    """Test that the home route returns a valid HTML response."""
    app = create_app()
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'QuickeeParts' in resp.data
    assert b'The parts utility' in resp.data


def test_create_app_with_config_dict():
    """Test that create_app properly overrides config when a dict is passed."""
    app = create_app({'SECRET_KEY': 'custom-secret'})
    assert app.config['SECRET_KEY'] == 'custom-secret'


def test_db_initialized():
    """Test that the db object is properly initialized as a SQLAlchemy instance."""
    assert db is not None
    from flask_sqlalchemy import SQLAlchemy
    assert isinstance(db, SQLAlchemy)


def test_create_app_with_config_class():
    """Test that create_app properly loads config from a class."""
    class Config:
        SECRET_KEY = 'class-based-secret'
    app = create_app(Config)
    assert app.config['SECRET_KEY'] == 'class-based-secret'


def test_imports_at_top_of_file():
    """Test that Flask and Flask-SQLAlchemy are imported at the top."""
    import ast
    with open('app.py') as f:
        tree = ast.parse(f.read())
    imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
    flask_import = any(isinstance(n, ast.ImportFrom) and n.module == 'flask' for n in imports)
    sqlalchemy_import = any(isinstance(n, ast.ImportFrom) and n.module == 'flask_sqlalchemy' for n in imports)
    assert flask_import, "Flask should be imported at top of app.py"
    assert sqlalchemy_import, "Flask-SQLAlchemy should be imported at top of app.py"
