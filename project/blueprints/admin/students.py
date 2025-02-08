from .head import *
import pandas as pd
from datetime import datetime

@admin.route('/students')
@login_required
def view_students():
    studentform = StudentForm()
    classform = ClassroomForm()
    importForm = UploadForm()
    students = Student.query.all()
    return render_template('admin/students.html' ,pageTitle="Students",students=students, form=studentform , classform=classform , importForm=importForm)

@admin.route('students/add_update_student', methods=['POST']) 
@login_required
def add_update_student():
    studentform = StudentForm()
    
    
    # Print the values of the form fields
    email = studentform.student_id.data+"@hostmail.com"
    username=studentform.firstname.data+"."+studentform.lastname.data
    if studentform.id.data:# Update existing user
        user = User.query.filter_by(id=studentform.id.data).first()

        user.student.student_id = studentform.student_id.data
        user.profile.first_name = studentform.firstname.data
        user.profile.last_name = studentform.lastname.data
        user.profile.sex = studentform.sex.data
        user.profile.date_of_birth = studentform.dob.data

        db.session.add(user)
        db.session.commit()
        flash('Student Updated successfully!', 'success')
        return redirect(url_for('admin.view_students'))
    else:  
        try:
            student_role = Role.query.filter_by(name='Student').first()
            new_user = User(username=username, email=email, password=generate_password_hash("password") , role=student_role )

            new_user.profile.first_name = studentform.firstname.data
            new_user.profile.last_name = studentform.lastname.data
            new_user.profile.sex = studentform.sex.data
            new_user.profile.date_of_birth = studentform.dob.data

            new_user.student.student_id = studentform.student_id.data
            db.session.add(new_user)
            db.session.commit()
            flash('Student added successfully!', 'success')
            return redirect(url_for('admin.view_students'))
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('admin.view_students'))


    # print(studentform.errors)
    # all_errors = []
    # for field, errors in studentform.errors.items():
    #     for error in errors:
    #         all_errors.append(f"<b>{studentform[field].label.text}: </b>{error}")
    
    # Flash the concatenated error messages
    # flash("<br>".join(all_errors), "danger")
    return redirect(url_for('admin.view_students'))


@admin.route('/students/changeclassroom', methods=['POST'])
def change_classroom():
    classroomform = ClassroomForm()

    if classroomform.validate_on_submit:
        classroom = Class.query.filter_by(level=classroomform.level.data, section=classroomform.section.data, group=classroomform.group.data).first()
        user = User.query.filter_by(id=classroomform.studentid.data).first()
        user.student.class_ =classroom
        db.session.add(user)
        db.session.commit()

        flash('Student Classroom Updated successfully!', 'success')
        return redirect(url_for('admin.view_students'))

@admin.route('/students/delete', methods=['POST'])
def delete_student():
    pass

@admin.route('/student/<int:student_id>/edit', methods=['GET', 'POST'])
def student_details(student_id):
    pass

@admin.route('/student/<int:student_id>/details', methods=['GET'])
def get_ustudent_details(student_id):
    pass


@admin.route('/student/import', methods=['POST'])
def import_students():
    form  = UploadForm()
    if form.validate_on_submit():
        file = form.file.data  # Get the uploaded file
        df = pd.read_excel(file, dtype=str)  # Read as string to avoid issues

        # Print each row
        for index, row in df.iterrows():
            email = row['Student_id']+"@hostmail.com"
            username= f"{row['firstname']}.{row['lastname']}{index}"
            student_role = Role.query.filter_by(name='Student').first()
            
            new_user = User(username=username, email=email, password=generate_password_hash("password") , role=student_role )

            new_user.profile.first_name = row['firstname']
            new_user.profile.last_name = row['lastname']
            new_user.profile.sex = row['sex']
            new_user.profile.date_of_birth = datetime.strptime(row['date_of_birth'], "%Y-%m-%d").date()

            new_user.student.student_id = row['Student_id']

            classroom = Class.query.filter_by(level=row['level'], section=row['section'], group=row['group']).first()

            if classroom:
                new_user.student.class_ =classroom


            db.session.add(new_user)
        
        db.session.commit()
        
        flash('File uploaded successfully!', 'success')
        return redirect(url_for('admin.view_students'))  # Redirect to an appropriate page

    flash('File upload failed. Please try again.', 'danger')
    return redirect(url_for('admin.view_students'))  # Redirect to an appropriate page
