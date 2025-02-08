

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField , TextAreaField , DateTimeField , FileField , EmailField , SelectField
from wtforms.validators import DataRequired, Email , Length , EqualTo ,ValidationError , Optional
from flask_wtf.file import FileAllowed
import re


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# Custom validator function for password complexity
def password_complexity(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not re.search(r'[a-z]', password):
        raise ValidationError('Password must contain at least one lowercase letter (a-z).')
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Password must contain at least one uppercase letter (A-Z).')
    if not re.search(r'[0-9]', password):
        raise ValidationError('Password must contain at least one number (0-9).')

class SignupForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    # password = PasswordField('Password', validators=[
    #     password_complexity,  # Add custom password complexity validator
    #     EqualTo('confirm', message='Passwords must match')
    # ])
    role = SelectField('Role', choices=[('', 'Choose your role'), ('1', 'Admin'), ('2', 'Teacher'), ('3', 'Supervisor')], 
                       validators=[DataRequired()], default='')
    password = PasswordField('Password',id="password-input", validators=[DataRequired()])
    confirm = PasswordField('Confirm Password',id="confirm-password-input",  validators=[DataRequired()])
    submit = SubmitField('Sign Up')