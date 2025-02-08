from .admin import admin  # Import the admin blueprint
from .auth import auth  # Import the auth blueprint
from .profile import profile  # Import the auth blueprint



blueprints = [
                ("/admin",admin), 
                ("/",auth),
                ("/",profile)
            ]