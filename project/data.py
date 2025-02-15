from .models import Role,User,Class,Profile,Subject
from werkzeug.security import generate_password_hash

def data(db):
    # Create roles if they don't exist
    admin_role = Role.query.filter_by(name='Admin').first()
    if admin_role is None:
        admin_role = Role(name='Admin')
        db.session.add(admin_role)
    
    teacher_role = Role.query.filter_by(name='Teacher').first()
    if teacher_role is None:
        teacher_role = Role(name='Teacher')
        db.session.add(teacher_role)

    supervisor_role = Role.query.filter_by(name='Supervisor').first()
    if supervisor_role is None:
        supervisor_role = Role(name='Supervisor')
        db.session.add(supervisor_role)
    
    student_role = Role.query.filter_by(name='Student').first()
    if student_role is None:
        student_role = Role(name='Student')
        db.session.add(student_role)


    admin_user = User.query.filter_by(username='admin').first()
    if admin_user is None:
        admin_user = User(username='admin', email='admin@example.com', password=generate_password_hash("admin") , role=admin_role )
        db.session.add(admin_user)

    Supervisor_user = User.query.filter_by(username='supervisor1').first()
    if Supervisor_user is None:
        Supervisor_user = User(username='supervisor1', email='supervisor1@example.com', password=generate_password_hash("supervisor1") , role=supervisor_role )
        db.session.add(Supervisor_user)
    
    Supervisor_user2 = User.query.filter_by(username='supervisor2').first()
    if Supervisor_user2 is None:
        Supervisor_user2 = User(username='supervisor2', email='supervisor2@example.com', password=generate_password_hash("supervisor2") , role=supervisor_role )
        db.session.add(Supervisor_user2)

    Supervisor_user3 = User.query.filter_by(username='supervisor3').first()
    if Supervisor_user3 is None:
        Supervisor_user3 = User(username='supervisor3', email='supervisor3@example.com', password=generate_password_hash("supervisor3") , role=supervisor_role )
        db.session.add(Supervisor_user3)

    teacher_user = User.query.filter_by(username='teacher1').first()
    if teacher_user is None:
        teacher_user = User(username='teacher1', email='teacher1@example.com', password=generate_password_hash("teacher1") , role=teacher_role )
        teacher_user.profile.first_name = 'ahmed'
        teacher_user.profile.last_name = 'nezar'
        db.session.add(teacher_user)
    
    teacher_user2 = User.query.filter_by(username='teacher2').first()
    if teacher_user2 is None:
        teacher_user2 = User(username='teacher2', email='teacher2@example.com', password=generate_password_hash("teacher2") , role=teacher_role )
        teacher_user2.profile.first_name = 'anis'
        teacher_user2.profile.last_name = 'bouzid'
        db.session.add(teacher_user2)

    teacher_user3 = User.query.filter_by(username='teacher3').first()
    if teacher_user3 is None:
        teacher_user3 = User(username='teacher3', email='teacher3@example.com', password=generate_password_hash("teacher3") , role=teacher_role )
        teacher_user3.profile.first_name = 'fatima'
        teacher_user3.profile.last_name = 'saada'
        db.session.add(teacher_user3)

    student1 = User.query.filter_by(username='student1').first()
    if student1 is None:
        student1 = User(username='student1', email='student1@example.com', password=generate_password_hash("student1") , role=student_role )
        student1.profile.first_name = "Imad"
        student1.profile.last_name = "Hafsi"
        student1.profile.sex = "Male"
        db.session.add(student1)
    
    student2 = User.query.filter_by(username='student2').first()
    if student2 is None:
        student2 = User(username='student2', email='student2@example.com', password=generate_password_hash("student2") , role=student_role )
        student2.profile.first_name = "Sana"
        student2.profile.last_name = "Hafsi"
        student2.profile.sex = "Female"
        db.session.add(student2)


    classes = [
        Class(level=1, section="Common trunk literature", group=1),
        Class(level=1, section="Common trunk literature", group=2),
        Class(level=1, section="Common trunk literature", group=3),
        Class(level=1, section="Common trunk science and technology", group=1),
        Class(level=1, section="Common trunk science and technology", group=2),
        Class(level=1, section="Common trunk science and technology", group=3),
        Class(level=2, section="Experimental sciences", group=1),
        Class(level=2, section="Experimental sciences", group=2),
        Class(level=2, section="Experimental sciences", group=3),
        Class(level=3, section="Experimental sciences", group=1),
        Class(level=3, section="Experimental sciences", group=2),
        Class(level=3, section="Experimental sciences", group=3),
        Class(level=2, section="Literature and philosophy", group=1),
        Class(level=2, section="Literature and philosophy", group=2),
        Class(level=3, section="Literature and philosophy", group=1),
        Class(level=3, section="Literature and philosophy", group=2),
        Class(level=2, section="Management and economy", group=1),
        Class(level=3, section="Management and economy", group=1),
        Class(level=2, section="Foreign languages", group=1),
        Class(level=3, section="Foreign languages", group=1),
        Class(level=2, section="Mathematics", group=1),
        Class(level=3, section="Mathematics", group=1),
        Class(level=2, section="Science Technology", group=1),
        Class(level=3, section="Science Technology", group=1),
    ]

    db.session.add_all(classes)

    subject_names = [
        "Mathematics", "Physics", "Natural Sciences", "Arabic Language and Literature", 
        "French Language", "English Language", "Philosophy", "Islamic Education", 
        "History and Geography", "Technology (Electrical Engineering)", 
        "Technology (Mechanical Engineering)", "Technology (Civil Engineering)", 
        "Technology (Process Engineering)", "Amazigh Language", "Spanish Language", 
        "German Language"
    ]

    subjects = [Subject(name=name) for name in subject_names]
    db.session.add_all(subjects)


    db.session.commit()