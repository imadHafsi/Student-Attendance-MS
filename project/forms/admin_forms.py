from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField,HiddenField,PasswordField,SelectMultipleField,DateField,FileField
from wtforms.validators import DataRequired, Email,ValidationError,EqualTo,Optional
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

class UserForm(FlaskForm):
    id = HiddenField('id')
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('', 'Choose your role'), ('1', 'Admin'), ('2', 'Teacher'), ('3', 'Supervisor'), ('4', 'Student')], 
                       validators=[DataRequired()], default='')
    status = SelectField('Status', choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    submit = SubmitField('Submit')


class PermissionForm(FlaskForm):
    csrf_token = StringField(validators=[DataRequired()], render_kw={'id': 'csrf_token_PermissionForm'})
    # Dynamically generate checkboxes for permissions
    submit = SubmitField('Update',name="PermissionRoleForm")

class adminChangePasswordForm(FlaskForm):
    csrf_token = StringField(validators=[DataRequired()], render_kw={'id': 'csrf_token_form_b'})
    newpassword = PasswordField('Password', validators=[
        password_complexity,  # Add custom password complexity validator
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')




class ClassForm(FlaskForm):
    id = HiddenField('id')
    level = SelectField('Level', choices=[('', 'Choose The level'), ('1', '1'), ('2', '2'), ('3', '3')], 
                       validators=[DataRequired()], default='')
    section = StringField('Section', validators=[DataRequired()])
    group = StringField('Group', validators=[DataRequired()])
    supervisors = SelectField("Supervisor", coerce=int, validators=[Optional()])
    submit = SubmitField('Submit')



class StudentForm(FlaskForm):
    id = HiddenField('id')
    student_id = StringField('Student id')
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    sex = SelectField('Sex', choices=[('Male', 'Male'), ('Female', 'Female')])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Submit')

class TeacherForm(FlaskForm):
    id = HiddenField('id')
    teacher_id = StringField('teacher id')
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    sex = SelectField('Sex', choices=[('Male', 'Male'), ('Female', 'Female')])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[Optional()])
    subjects = SelectField("Subjects", coerce=int, validators=[Optional()])
    submit = SubmitField('Submit')

class AssignClassForm(FlaskForm):
    tid = HiddenField('tid')
    classes = SelectMultipleField(
        "Assign Classes", 
        coerce=int, 
        validators=[Optional()]
    )  # Multi-select field for classes

    submit = SubmitField("Assign Classes")

class SupervisorForm(FlaskForm):
    id = HiddenField('id')
    supervisor_id = StringField('supervisor id')
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    sex = SelectField('Sex', choices=[('Male', 'Male'), ('Female', 'Female')])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Submit')


class ClassroomForm(FlaskForm):
    studentid = HiddenField('studentid')
    level = SelectField('Level', choices=[('', 'Choose The level'), ('1', '1'), ('2', '2'), ('3', '3')], 
                       validators=[DataRequired()], default='')
    section = SelectField('Section', validators=[DataRequired()])
    group = SelectField('Group', validators=[DataRequired()])
    submit = SubmitField('Submit')



class UploadForm(FlaskForm):
    file = FileField('Select Excel File', validators=[DataRequired()])
    submit = SubmitField('Upload')