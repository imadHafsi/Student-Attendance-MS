from flask import Blueprint



auth  = Blueprint('auth',__name__,template_folder='templates',static_folder='static',)

@auth.route('/login')
def login():
    return 'this is page login'