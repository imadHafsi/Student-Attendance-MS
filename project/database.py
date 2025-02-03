from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
migrate = Migrate()  # Define Migrate globally

def init_db(app):
    """Initialize database with the Flask app."""
    db.init_app(app)
    migrate.init_app(app, db)  # Bind Flask-Migrate to app and db

def create_database():
    """Create database tables if they do not exist."""
    from .models import User
    db.create_all()
    # Create users if they don't exist
    admin_user = User.query.filter_by(username='admin').first()
    if admin_user is None:
        admin_user = User(username='admin', password=generate_password_hash("admin"))
        db.session.add(admin_user)
        db.session.commit()