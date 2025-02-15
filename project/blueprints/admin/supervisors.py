from .head import *



@admin.route('/supervisors')
@login_required
def view_supervisors():
    supervisorForm = SupervisorForm()
    supervisors = Supervisor.query.all()
    assignclassesForm = AssignClassForm()
    return render_template('admin/supervisors.html' ,pageTitle="Supervisors",supervisors=supervisors, form=supervisorForm , assignclassesForm=assignclassesForm)

@admin.route('supervisors/add_update_supervisor', methods=['POST']) 
@login_required
def add_update_supervisor():
    supervisorForm = SupervisorForm()
    if supervisorForm.validate_on_submit():
        try:
             if supervisorForm.id.data:
                user = User.query.filter_by(id = supervisorForm.id.data).first()
                user.supervisor.supervisor_id = supervisorForm.supervisor_id.data
                user.profile.first_name = supervisorForm.firstname.data
                user.profile.last_name = supervisorForm.lastname.data
                user.profile.sex = supervisorForm.sex.data
                user.profile.date_of_birth = supervisorForm.dob.data
                db.session.commit()
                flash('Supervisor updated successfully!', 'success')
             else:
                 print(supervisorForm.subjects.data)
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('admin.view_supervisors'))
    else:
        all_errors = []
        for field, errors in supervisorForm.errors.items():
            for error in errors:
                all_errors.append(f"<b>{supervisorForm[field].label.text}: </b>{error}")
        
        # Flash the concatenated error messages
        flash("<br>".join(all_errors), "danger")

    return redirect(url_for('admin.view_supervisors'))


@admin.route('supervisors/classes_to_assign', methods=['POST']) 
@login_required
def classes_to_assign_supervisors():
    assignclassesForm = AssignClassForm()
    classes = Class.query.all()
    assignclassesForm.classes.choices = [cls.id for cls in classes]
    print(assignclassesForm.tid)
    if assignclassesForm.validate_on_submit():
        try:
            classes_to_update = Class.query.filter_by(supervisor_id=assignclassesForm.tid.data).all()
            # Update the supervisor_id to None for each class found
            for class_instance in classes_to_update:
                class_instance.supervisor_id = None

            for class_id in assignclassesForm.classes.data:
                classe = Class.query.get(class_id)
                classe.supervisor_id = assignclassesForm.tid.data
                db.session.add(classe)
            
            db.session.commit()
            flash("Classes assigned successfully!", "success")
            return redirect(url_for('admin.view_supervisors'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('admin.view_supervisors'))
    
    else:
        all_errors = []
        for field, errors in assignclassesForm.errors.items():
            for error in errors:
                all_errors.append(f"<b>{assignclassesForm[field].label.text}: </b>{error}")
        
        # Flash the concatenated error messages
        flash("<br>".join(all_errors), "danger")

    return redirect(url_for('admin.view_supervisors'))