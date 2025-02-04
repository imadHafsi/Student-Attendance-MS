from .models import Role,User,Class
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
    


    class111 = Class(level=1,section="Common trunk literature",group=1)
    class112 = Class(level=1,section="Common trunk literature",group=2)

    class121 = Class(level=1,section="Common trunk science and technology",group=1)
    class122 = Class(level=1,section="Common trunk science and technology",group=2)
    class123 = Class(level=1,section="Common trunk science and technology",group=3)

    class211 = Class(level=2,section="Experimental sciences",group=1)
    class212 = Class(level=2,section="Experimental sciences",group=2)
    class213 = Class(level=2,section="Experimental sciences",group=3)

    class311 = Class(level=3,section="Experimental sciences",group=1)
    class312 = Class(level=3,section="Experimental sciences",group=2)
    class313 = Class(level=3,section="Experimental sciences",group=3)

    class221 = Class(level=2,section="Literature and philosophy",group=1)
    class222 = Class(level=2,section="Literature and philosophy",group=2)

    class321 = Class(level=3,section="Literature and philosophy",group=1)
    class322 = Class(level=3,section="Literature and philosophy",group=2)

    class231 = Class(level=2,section="Management and economy",group=1)
    class331 = Class(level=3,section="Management and economy",group=1)

    class241 = Class(level=2,section="Foreign languages",group=1)
    class341 = Class(level=3,section="Foreign languages",group=1)

    class251 = Class(level=2,section="Mathematics",group=1)
    class351 = Class(level=3,section="Mathematics",group=1)

    class261 = Class(level=2,section="Science Technology",group=1)
    class361 = Class(level=3,section="Science Technology",group=1)






    db.session.add(class111)
    db.session.add(class112)
    db.session.add(class121)
    db.session.add(class122)
    db.session.add(class123)
    db.session.add(class211)
    db.session.add(class212)
    db.session.add(class213)
    db.session.add(class311)
    db.session.add(class312)
    db.session.add(class313)
    db.session.add(class221)
    db.session.add(class222)
    db.session.add(class321)
    db.session.add(class322)
    db.session.add(class231)
    db.session.add(class331)
    db.session.add(class241)
    db.session.add(class341)
    db.session.add(class251)
    db.session.add(class351)
    db.session.add(class261)
    db.session.add(class361)

    
    db.session.commit()