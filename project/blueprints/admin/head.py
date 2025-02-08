from flask import Blueprint , flash , redirect , url_for , render_template,jsonify,request
from ...database import db
from flask_login import login_required
from  ...forms import UserForm , ClassForm , StudentForm , ClassroomForm , UploadForm
from project.models import User,Role,Class,Student
from werkzeug.security import generate_password_hash


admin = Blueprint('admin',__name__,template_folder='templates',static_folder='static',)
