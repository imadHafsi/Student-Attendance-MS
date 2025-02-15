from .head import *



@admin.route('/classes')
@login_required
def view_classes():
    classform = ClassForm()

    supervisors = User.query.join(Role).filter(Role.name == "Supervisor").all()
    # Populate choices as a list of tuples (user_id, user_name)
    classform.supervisors.choices = [(0, "Select a supervisor")]+[(s.id, s.username) for s in supervisors]

    classes = Class.query.all()
    return render_template('admin/classes.html' ,pageTitle="Classes",classes=classes, form=classform)


@admin.route('/classes/delete', methods=['POST'])
def delete_class():
    class_id = request.form.get('class_id')
    classroom = Class.query.get(class_id)
    if classroom:
        try:

            # Delete the user
            db.session.delete(classroom)
            db.session.commit()
            flash('Class deleted successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting Class: {str(e)}', 'danger')
    else:
        flash('Class not found', 'danger')
    return redirect(url_for('admin.view_classes'))


@admin.route('/classes/add_update_class', methods=['POST'])
@login_required
def add_update_class():
    form = ClassForm()
    supervisors = User.query.join(Role).filter(Role.name == "Supervisor").all()
    form.supervisors.choices = [(0, "Select a supervisor")]+[(s.id, s.username) for s in supervisors]

    if form.validate_on_submit():
        try:
            #print(form.id.data)

            selected_supervisor_id = form.supervisors.data  # Get selected supervisor ID


            if form.id.data:  # Update existing user
                classroom = Class.query.get(form.id.data)

                classroom.level=form.level.data
                classroom.section=form.section.data
                classroom.group=form.group.data
                classroom.supervisor_id = selected_supervisor_id
                db.session.commit()
                flash('Class updated successfully!', 'success')

            else:  # Add new user
                
                new_class = Class(
                    level=form.level.data,
                    section=form.section.data,
                    group=form.group.data,
                    supervisor_id = selected_supervisor_id
                )

                db.session.add(new_class)
                db.session.commit()
                flash('Class added successfully!', 'success')
            
            return redirect(url_for('admin.view_classes'))
        except Exception as e:
                flash(f'Error: {str(e)}', 'danger')
                return redirect(url_for('admin.view_classes'))
    
    print(form.errors)
    all_errors = []
    for field, errors in form.errors.items():
        for error in errors:
            all_errors.append(f"<b>{form[field].label.text}: </b>{error}")
    
    # Flash the concatenated error messages
    flash("<br>".join(all_errors), "danger")
    return redirect(url_for('admin.view_classes'))