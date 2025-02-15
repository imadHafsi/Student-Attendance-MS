from .head import *


@admin.route('/teachers')
@login_required
def view_teachers():
    teacherform = TeacherForm()
    assignclassesForm = AssignClassForm()
    subjects = Subject.query.all()
    teachers = Teacher.query.all()

    teacherform.subjects.choices = [(0, "Select Subject")]+[(s.id, s.name) for s in subjects]

    return render_template(
        'admin/teachers.html',
        pageTitle="Teachers",
        teachers=teachers,
        form=teacherform,
        assignclassesForm=assignclassesForm,
    )

@admin.route('teachers/add_update_teacher', methods=['POST']) 
@login_required
def add_update_teacher():
    teacherForm = TeacherForm()
    subjects = Subject.query.all()
    teacherForm.subjects.choices = [(0, "Select Subject")]+[(s.id, s.name) for s in subjects]
    if teacherForm.validate_on_submit():
        try:
             if teacherForm.id.data:
                user = User.query.filter_by(id = teacherForm.id.data).first()
                user.teacher.teacher_id = teacherForm.teacher_id.data
                user.profile.first_name = teacherForm.firstname.data
                user.profile.last_name = teacherForm.lastname.data
                user.profile.sex = teacherForm.sex.data
                user.profile.date_of_birth = teacherForm.dob.data
                user.teacher.subject_id = teacherForm.subjects.data

                db.session.commit()
                flash('Teacher updated successfully!', 'success')
             else:
                 print(teacherForm.subjects.data)
        except Exception as e:
            
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('admin.view_teachers'))
    else:
        print(teacherForm.dob.data)
        all_errors = []
        for field, errors in teacherForm.errors.items():
            for error in errors:
                all_errors.append(f"<b>{teacherForm[field].label.text}: </b>{error}")
        
        # Flash the concatenated error messages
        flash("<br>".join(all_errors), "danger")

    return redirect(url_for('admin.view_teachers'))


@admin.route('teachers/classes_to_assign', methods=['POST']) 
@login_required
def classes_to_assign():
    assignclassesForm = AssignClassForm()
    classes = Class.query.all()
    assignclassesForm.classes.choices = [cls.id for cls in classes]

    if assignclassesForm.validate_on_submit():
        try:
            db.session.query(TeacherClass).filter_by(teacher_id=assignclassesForm.tid.data).delete()
            for class_id in assignclassesForm.classes.data:
                new_class_teacher = TeacherClass(
                        teacher_id=assignclassesForm.tid.data,
                        class_id=class_id
                    )

                db.session.add(new_class_teacher)
            
            db.session.commit()
            flash("Classes assigned successfully!", "success")
            return redirect(url_for('admin.view_teachers'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('admin.view_teachers'))
    
    else:
        all_errors = []
        for field, errors in assignclassesForm.errors.items():
            for error in errors:
                all_errors.append(f"<b>{assignclassesForm[field].label.text}: </b>{error}")
        
        # Flash the concatenated error messages
        flash("<br>".join(all_errors), "danger")

    return redirect(url_for('admin.view_teachers'))


