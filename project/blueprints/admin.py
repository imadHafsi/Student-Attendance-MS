from flask import Blueprint,render_template
from flask_login import login_required


admin = Blueprint('admin',__name__,template_folder='templates',static_folder='static',)


@admin.route('/')
@login_required
def dashboard():
    return render_template('admin.html',title="Admin Page")