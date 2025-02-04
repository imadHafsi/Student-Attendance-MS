from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()  # Define Migrate globally

def init_db(app):
    """Initialize database with the Flask app."""
    db.init_app(app)
    migrate.init_app(app, db)  # Bind Flask-Migrate to app and db

def create_database():
    """Create database tables if they do not exist."""
    from .models import User,Role,Class
    db.drop_all()
    db.create_all()

    from .data import data
    data(db)
    