
import os
from flask import Flask
from flask_login import LoginManager
from flask_talisman import Talisman

from .config import DevelopmentConfig, ProductionConfig, TestingConfig
from .database import db, init_db, create_database


def create_app():

    app = Flask(__name__)

    # Choose config based on environment
    env = os.getenv('FLASK_ENV', 'development')

    if env == 'production':
        app.config.from_object(ProductionConfig)
    elif env == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    
    # Initialize database
    init_db(app)

    with app.app_context():
        create_database()  # Create tables inside application context

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

        # Define your CSP
    csp = {
    'default-src': ['\'self\'','https://cdn.lordicon.com',
                    'https://cdn.datatables.net',
                    'https://cdnjs.cloudflare.com'
                    ],
    'script-src': [
                    '\'self\'',
                     '\'unsafe-eval\'',
                    'https://cdn.jsdelivr.net',
                    'https://cdn.lordicon.com',
                    'https://cdn.datatables.net',
                    'https://cdnjs.cloudflare.com',
                    'https://code.jquery.com'  # Add jQuery CDN
                ],
    'style-src': ['\'self\' \'unsafe-inline\'','https://cdn.lordicon.com','https://fonts.googleapis.com','https://cdn.datatables.net'],
    'img-src': ['\'self\' data:','https://cdn.lordicon.com'],
    'font-src': ['\'self\' data:','https://fonts.gstatic.com','https://cdn.lordicon.com']
    }

    # Enable Flask-Talisman with the CSP
    Talisman(app, content_security_policy=csp,strict_transport_security=True, strict_transport_security_max_age=31536000,content_security_policy_nonce_in=['script-src'])
    
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)) 
    

    from .blueprints.admin import admin
    from .blueprints.auth import auth

    app.register_blueprint(admin , url_prefix='/admin')
    app.register_blueprint(auth , url_prefix='/')


    return app