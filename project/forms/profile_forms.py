from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField , TextAreaField , DateTimeField , FileField , EmailField , SelectField
from wtforms.validators import DataRequired, Email , Length , EqualTo ,ValidationError , Optional
from flask_wtf.file import FileAllowed
import re

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
    
    

class personalDetailsForm(FlaskForm):
    csrf_token = StringField(validators=[DataRequired()], render_kw={'id': 'csrf_token_form_a'})
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    phonenumber = StringField('Phone Number')
    email= EmailField('Email', validators=[DataRequired(), Email()])
    dob = DateTimeField('Date of Birth', format='%d %b, %Y', validators=[Optional()])
    address = TextAreaField('Address')
    submit = SubmitField('Update')

class changePasswordForm(FlaskForm):
    csrf_token = StringField(validators=[DataRequired()], render_kw={'id': 'csrf_token_form_b'})
    oldpassword = PasswordField('Password', validators=[DataRequired("The old password is required")])
    newpassword = PasswordField('Password', validators=[
        password_complexity,  # Add custom password complexity validator
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')

class deleteAvatarForm(FlaskForm):
    csrf_token = StringField(validators=[DataRequired()], render_kw={'id': 'csrf_token_deleteAvatarForm'})
    submit = SubmitField('Delete Avatar')

class AvatarUploadForm(FlaskForm):
    csrf_token = StringField(validators=[DataRequired()], render_kw={'id': 'csrf_token_AvatarUploadForm'})
    avatar = FileField('Avatar', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Upload Avatar')


class DeleteAccountForm(FlaskForm):
    csrf_token = StringField(render_kw={'id': 'csrf_token_DeleteAccountForm'})
    password_d = PasswordField('Password', validators=[DataRequired('password is required')])
    submit = SubmitField('Close & Delete This Account')
