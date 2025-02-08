from datetime import datetime, timedelta,timezone

from flask import Blueprint , session , flash , redirect , url_for , render_template , request
from flask_login import login_user,logout_user,login_required , current_user
from werkzeug.security import generate_password_hash,check_password_hash
from ..database import db
from ..models import User,Role
from ..forms import LoginForm , SignupForm
from ..utils import redirect_based_on_role

auth  = Blueprint('auth',__name__,template_folder='templates',static_folder='static',)

@auth.route('/')
def index():
    """Redirect based on role """
    #return redirect_based_on_role()
    return render_template('user-base.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['POST', 'GET'])
def login():
    """Handle user login.This function manages the login process for users
    """
    
    if current_user.is_authenticated:
        return redirect_based_on_role()

    form = LoginForm()
    
     # Get the failed login attempts and last attempt time from session
    failed_attempts = session.get('failed_login_attempts', 0)
    last_attempt_time = session.get('last_attempt_time')

    # Check if 10 minutes have passed since the last failed attempt
    if last_attempt_time and datetime.now(timezone.utc) - last_attempt_time > timedelta(minutes=10):
        failed_attempts = 0
        session['failed_login_attempts'] = 0

    if form.validate_on_submit():  # Validate the form submission
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        if failed_attempts >= 4:
            flash("Too many login attempts. Please try again later.", 'danger')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(email=email).first()

        if not user:
            user = User.query.filter_by(username=email).first()

        if not user or not check_password_hash(user.password, password):
            failed_attempts += 1
            session['failed_login_attempts'] = failed_attempts
            session['last_attempt_time'] = datetime.now(timezone.utc)
            flash("Invalid Credentials", 'danger')
            flash(f"{failed_attempts} attempts from 4 attempts", 'warning')
            return redirect(url_for('auth.login'))

        if user.status.value == "Inactive":
            flash("Your account is Deactivated", 'warning')
            return redirect(url_for('auth.login'))
        

        # On successful login, reset the failed attempts counter
        session['failed_login_attempts'] = 0
        session['last_attempt_time'] = None

        login_user(user, remember=remember)

        if current_user.is_authenticated:
            return redirect_based_on_role()
        
    return render_template('account/login.html', form=form)


@auth.route('/signup',methods=['POST',"GET"])  
def signup():
    
    if current_user.is_authenticated:
        return redirect_based_on_role()
    
    form = SignupForm()


    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        role_id = int(form.role.data)
        password = form.password.data


        user_email = User.query.filter_by(email=email).first()
        user_username = User.query.filter_by(username=username).first()
        role = Role.query.get(role_id)    
        
        

        if user_email:
            flash("User email already Exists",'danger')
            return redirect(url_for('auth.signup'))
        if user_username:    
            flash("Username already Exists",'danger')
            return redirect(url_for('auth.signup')) 
        if not role:    
            flash('Invalid role selected', 'danger')
            return redirect(url_for('auth.signup'))
        

        new_user = User(email=email,username=username,password=generate_password_hash(password), role=role )


        db.session.add(new_user)
        db.session.commit()

        flash('Your account is created successfully', 'success')
        return redirect(url_for('auth.login'))
    return render_template('account/signup.html',form=form)

@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    pass
    # forgotPassform = forgotPasswordForm()
    
    # if request.method == 'POST':
    #     email = forgotPassform.email.data
    #     user = User.query.filter_by(email=email).first()
        
    #     if user:
    #         token = generate_reset_token(user.email)
    #         reset_url = url_for('auth.reset_password', token=token, _external=True)
    #         send_reset_email(user.email, reset_url)
    #         flash('A password reset link has been sent to your email address.', 'info')
    #         return render_template('account/auth-success.html')
    #     else:
    #         flash('No account with that email address exists.', 'danger')
    #         return redirect(url_for('auth.forgot_password'))
    
    # return render_template('account/forgot_password.html',form=forgotPassform)


@auth.route('/profile/delete-account',methods=['POST'])
@login_required
def delete_account():
    pass