from flask_login import UserMixin
from . import db




class User(db.Model , UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(20),unique=True)
    password = db.Column(db.String(50),nullable=False)