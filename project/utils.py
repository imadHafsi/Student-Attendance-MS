import os,uuid
from flask_login import current_user
from flask import redirect, url_for , abort

def redirect_based_on_role():
    '''reidrect function'''
    if current_user.is_authenticated:
        if current_user.role.name == 'Admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role.name == 'Supervisor':
            return "redirect(url_for('supervisor.dashboard_supervisor'))"
        elif current_user.role.name == 'Teacher':
            return "redirect(url_for('teacher.dashboard_teacher'))"
        elif current_user.role.name == 'Student':
            return "redirect(url_for('student.dashboard_student'))"

    # If not authenticated, go to login page
    return redirect(url_for('auth.login'))


def generate_unique_filename(filename):
    ext = os.path.splitext(filename)[1]
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    return unique_filename

ALLOWED_EXTENSIONS_AVATAR = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_AVATAR

def delete_previous_avatar(filename):
    if filename and filename!='default.jpg':  # Check if the filename is not empty or None
        file_path = os.path.join('project/static/uploads/avatars/', filename)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted old avatar: {filename}")
            else:
                print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error deleting file: {e}")

