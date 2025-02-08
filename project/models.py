from flask_login import UserMixin
from . import db
import enum
from datetime import datetime

# Define the ENUM type for role
class RoleEnum(enum.Enum):
    Admin = "Admin"
    Teacher = "Teacher"
    Supervisor = "Supervisor"
    Student = "Student"
    
class StatusEnum(enum.Enum):
    Active = "Active"
    Inactive = "Inactive"

class AttendanceStatus(enum.Enum):
    Present = "Present"
    Absent = "Absent"
    Late = "Late"  # Arrived after class started
    Excused = "Excused"  # Absent but has a valid excuse
    Unexcused = "Unexcused"  # Absent without a valid reason
    LeftEarly = "Left Early"  # Attended but left before the session ended
    Sick = "Sick"  # Absent due to illness
    Remote = "Remote"  # Attended remotely (online)


# Association table between roles and permissions
roles_permissions = db.Table('roles_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'))
)

# Association table between users and permissions (for individual permissions)
users_permissions = db.Table('users_permissions',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'))
)

# Association table between users and denied_permissions (for individual denied permissions)
users_denied_permissions = db.Table('users_denied_permissions',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'))
)

# Role model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.relationship('Permission', secondary=roles_permissions, backref=db.backref('roles', lazy='dynamic'))

    def __repr__(self):
        return f'<Role {self.name}>'

# Permission model
class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(200), nullable=True, default='')
    
    def __repr__(self):
        return f'<Permission {self.name}>'


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.Inactive, nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', backref='users')
    
    profile = db.relationship('Profile', uselist=False, backref='user', lazy='joined')


    individual_permissions = db.relationship('Permission', secondary=users_permissions, backref=db.backref('individual_users', lazy='dynamic'))
    denied_permissions = db.relationship('Permission', secondary=users_denied_permissions, backref=db.backref('denied_users', lazy='dynamic'))
    
    
    def __init__(self, email, username, password , role , status=StatusEnum.Active):
        self.email = email
        self.username = username
        self.password = password
        self.status = status
        self.role = role
        self.profile = Profile()

            # Automatically create a Student entry if the role is Student
        if role.name.lower() == "student":
            new_student = Student(user=self)
            db.session.add(new_student)



    def has_permission(self, permission_name):
        """Check if user has a specific permission, either through their role or individually."""
        # Check if the permission is granted by the role
        if any(permission.name == permission_name for permission in self.role.permissions):
            if any(permission.name == permission_name for permission in self.denied_permissions):
                return False
            else:
                return True
        
        # Check if the permission is granted directly to the user
        if any(permission.name == permission_name for permission in self.individual_permissions):
            return True
        return False

    def __repr__(self):
        return f'<User {self.username}>'
    
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=True, default='')
    last_name = db.Column(db.String(100), nullable=True, default='')
    sex = db.Column(db.String(100), nullable=True, default='')
    avatar = db.Column(db.String(200), nullable=True, default='default.jpg')
    date_of_birth = db.Column(db.Date, nullable=True)
    address = db.Column(db.String(200), nullable=True, default='')
    phone_number = db.Column(db.String(20), nullable=True, default='')
    
    # Foreign key to User model
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


# Association Table for Many-to-Many Relationship
teacher_class = db.Table(
    'teacher_class',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('classes.id'), primary_key=True)
)


# Class table
class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer,nullable=False)
    section = db.Column(db.String(100), nullable=False)
    group = db.Column(db.Integer,nullable=False)

    supervisor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    supervisor = db.relationship('User', backref='classes')

    teachers = db.relationship('Teacher', secondary=teacher_class, back_populates='classes')

    


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(100), unique=True)


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer , primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('teacher', uselist=False))
    subject = db.relationship('Subject', backref='teachers')

    classes = db.relationship('Class', secondary=teacher_class, back_populates='teachers')


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer , primary_key=True)
    student_id = db.Column(db.String(20) , unique = True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    user = db.relationship('User', backref=db.backref('student', uselist=False))

    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=True)
    class_ = db.relationship('Class', backref='students')


class Attendance(db.Model):
    __tablename__ = 'attendances'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)  # Student's attendance
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)  # Subject of attendance
    recordedby_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Who recorded attendance
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum(AttendanceStatus), nullable=False)

    # Relationships
    student = db.relationship('Student', backref='attendances')  # The student
    subject = db.relationship('Subject', backref='attendances')  # Subject attended
    recorded_by = db.relationship('User', foreign_keys=[recordedby_id], backref='recorded_attendances')  # Who recorded

