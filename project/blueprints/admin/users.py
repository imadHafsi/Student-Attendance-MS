from .head import *



@admin.route('/')
@login_required
def dashboard():
    return render_template('admin/index.html',pageTitle="Admin Dashboard")



@admin.route('/users')
@login_required
def view_users():
    userform = UserForm()
    users = User.query.all()
    return render_template('admin/users.html' ,pageTitle="Users",users=users, form=userform)

@admin.route('users/add_update_user', methods=['POST']) 
@login_required
def add_update_user():
    form = UserForm()
    if form.validate_on_submit():
        try:
            role = Role.query.get(int(form.role.data))
            print(form.id.data)
            if form.id.data:  # Update existing user
                user = User.query.get(form.id.data)
                if user:
                    if user.username != form.username.data:
                        user_username = User.query.filter_by(username=form.username.data).first()
                        if user_username:    
                            flash("Username already Exists",'danger')
                            return redirect(url_for('admin.view_users'))
                            

                    if user.email != form.email.data :
                        user_email = User.query.filter_by(email=form.email.data).first()
                        if user_email:
                            flash("User email already Exists",'danger')
                            return redirect(url_for('admin.view_users'))   


                    user.username = form.username.data
                    user.email = form.email.data                    
                    user.status = form.status.data

                    if role.name.lower() == "student" and user.role.name .lower() != "student":
                        user.role = role
                        new_student = Student(user=user)
                        db.session.add(new_student)
                    elif role.name.lower() != "student" and user.role.name .lower() == "student":
                        user.role = role
                        student = Student.query.filter_by(user_id=user.id).first()
                        db.session.delete(student)

                    db.session.commit()
                    flash('User updated successfully!', 'success')
            else:  # Add new user
                user_email = User.query.filter_by(email=form.email.data).first()
                user_username = User.query.filter_by(username=form.username.data).first()    
                
                if user_email:
                    flash("User email already Exists",'danger')
                    return redirect(url_for('admin.view_users'))
                if user_username:    
                    flash("Username already Exists",'danger')
                    return redirect(url_for('admin.view_users'))
                new_user = User(
                    username=form.username.data,
                    email=form.email.data,
                    password=generate_password_hash("password"),
                    status=form.status.data,
                    role=role
                )
                new_user.role=role
                db.session.add(new_user)
                db.session.commit()
                flash('User added successfully!', 'success')
            
            return redirect(url_for('admin.view_users'))
        except Exception as e:
                flash(f'Error: {str(e)}', 'danger')
                return redirect(url_for('admin.view_users'))
    
    print(form.errors)
    all_errors = []
    for field, errors in form.errors.items():
        for error in errors:
            all_errors.append(f"<b>{form[field].label.text}: </b>{error}")
    
    # Flash the concatenated error messages
    flash("<br>".join(all_errors), "danger")
    return redirect(url_for('admin.view_users'))


@admin.route('/users/delete', methods=['POST'])
def delete_user():
    pass

@admin.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
def user_details(user_id):
    pass

@admin.route('/user/<int:user_id>/details', methods=['GET'])
def get_user_details(user_id):
    user = User.query.get_or_404(user_id)
    user_data = {
        "username": user.username,
        "avatar": url_for('static', filename='uploads/avatars/' + user.profile.avatar),
        "email": user.email or "No email provided",
        "phone": user.profile.phone_number or "No phone number",
        "first_name": user.profile.first_name or "N/A",
        "last_name": user.profile.last_name or "N/A",
        "role": user.role.name or "No role assigned",
        "status": user.status.value if user.status else "Unknown status",
        # Add more fields as needed, like permissions
        "role_permissions": [perm.name for perm in user.role.permissions],
        "denied_permissions": [perm.name for perm in user.denied_permissions], 
        "ind_permissions": [perm.name for perm in user.individual_permissions] 
    }
    return jsonify(user_data)



