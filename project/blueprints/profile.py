''' Blueprint for handling common  operations among admin,supervisor,client'''
from datetime import datetime, timedelta,timezone
import os
from flask import Blueprint,render_template,request,redirect,url_for,flash,session,current_app
from flask_login import login_user,logout_user,login_required , current_user
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
#from project import limiter
from project.models import User,Profile
from project.database import db
from project.utils import redirect_based_on_role , generate_unique_filename ,allowed_file ,delete_previous_avatar
from ..forms import (
    personalDetailsForm,changePasswordForm,DeleteAccountForm,
    deleteAvatarForm,AvatarUploadForm
)

profile = Blueprint('profile',__name__,template_folder='templates',static_folder='static',)

#limiter.limit("10 per minute")(profile)
#login_limits=["5 per minute", "10 per 10 minutes"]
#signup_limits=["3 per minute", "10 per hour"]
#password_recovery_limits=["2 per minute", "5 per hour"]


@profile.route('/profile',methods=['POST','GET'])
@login_required
def profile_settings_edit():
    
    activetab = request.args.get('activetab', 'personalDetails')
    personalDetailForm = personalDetailsForm()
    changePassForm = changePasswordForm()
    deletAvatarForm = deleteAvatarForm()
    AvatarUploadeForm = AvatarUploadForm()
    DeleteAccounteForm = DeleteAccountForm()

    if request.method == 'GET':
        personalDetailForm.firstname.data = current_user.profile.first_name
        personalDetailForm.lastname.data = current_user.profile.last_name
        personalDetailForm.email.data = current_user.email
        personalDetailForm.address.data = current_user.profile.address
        personalDetailForm.phonenumber.data = current_user.profile.phone_number
        personalDetailForm.dob.data = current_user.profile.date_of_birth if current_user.profile.date_of_birth else ''
        
        return render_template('account/pages-profile-settings.html' , activetab=activetab ,
                               personalDetailForm=personalDetailForm , 
                               changePasswordForm=changePassForm , 
                               deleteAvatarForm=deletAvatarForm , 
                               AvatarUploadForm=AvatarUploadeForm,
                               DeleteAccounteForm=DeleteAccounteForm)


    if personalDetailForm.validate_on_submit():
        firstname = personalDetailForm.firstname.data
        lastname = personalDetailForm.lastname.data
        phonenumber = personalDetailForm.phonenumber.data
        email = personalDetailForm.email.data
        dob = personalDetailForm.dob.data
        address = personalDetailForm.address.data

        current_user.profile.first_name = firstname
        current_user.profile.last_name = lastname
        current_user.profile.phone_number = phonenumber
        current_user.profile.address = address
        current_user.email = email
        current_user.profile.date_of_birth = dob
        # Add any additional fields you want to update

        # Commit the changes to the database
        db.session.commit()
        flash('Personal Details successfuly updated', 'success')
        return redirect(url_for('profile.profile_settings_edit'))
    
    if changePassForm.validate_on_submit():

        old_password = changePassForm.oldpassword.data
        new_password = changePassForm.newpassword.data

        # Check if the old password is correct
        if check_password_hash(current_user.password, old_password):
            # Check if new password matches confirm password
                current_user.password = generate_password_hash(new_password)
                db.session.commit()
                flash('Password successfuly changed', 'success')
        else:
            # Handle case where old password is incorrect
            flash('Old password is incorrect', 'danger')
    
    return redirect(url_for('profile.profile_settings_edit', activetab="changePassword"))


@profile.route('/profile/upload-avatar', methods=['POST'])
def upload_avatar():
    print("it comes here")
    try:
        if 'avatar' not in request.files:
            flash('No file part', 'danger')
            return redirect(url_for('profile.profile_settings_edit'))
        
        file = request.files['avatar']
        
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(url_for('profile.profile_settings_edit'))
        
        if file and allowed_file(file.filename):
            filename = generate_unique_filename(secure_filename(file.filename))

            # Delete the old avatar if it exists
            if current_user.profile.avatar != 'default.jpg':
                delete_previous_avatar(current_user.profile.avatar)

            file.save(os.path.join('project/static/uploads/avatars/', filename))
            
            # Update the user's avatar in the database
            current_user.profile.avatar = filename
            db.session.commit()
            
            flash('Avatar uploaded successfully!', 'success')
            return redirect(url_for('profile.profile_settings_edit'))
        else:
            flash('Invalid file type. Only images are allowed.', 'danger')
            return redirect(url_for('profile.profile_settings_edit'))
    except Exception as e:
        print(e)
        flash('File upload failed.', 'danger')

    return redirect(url_for('profile.profile_settings_edit'))


@profile.route('/profile/delete-avatar', methods=['POST'])
def delete_avatar():
    if current_user.profile.avatar:
    # Delete the old avatar if it exists
        if current_user.profile.avatar != 'default.jpg':
            delete_previous_avatar(current_user.profile.avatar)
        current_user.profile.avatar = 'default.jpg'
        db.session.commit()
        flash('Avatar deleted successfully!','success')
        
    return redirect(url_for('profile.profile_settings_edit'))