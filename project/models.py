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
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.Inactive, nullable=False)
    role = db.relationship('Role', backref='users')
    
    individual_permissions = db.relationship('Permission', secondary=users_permissions, backref=db.backref('individual_users', lazy='dynamic'))
    denied_permissions = db.relationship('Permission', secondary=users_denied_permissions, backref=db.backref('denied_users', lazy='dynamic'))
    
    # One-to-One relationship with UserInfo
    user_info = db.relationship('UserInfo', backref='users', uselist=False)
    
    #teacher_classes = db.relationship('TeacherClass', backref='teacher', lazy=True)
    #supervised_classes = db.relationship('SupervisorClass', backref='supervisor', lazy=True)

    def __init__(self, email, username, password , role , status=StatusEnum.Inactive):
        self.email = email
        self.username = username
        self.password = password
        self.status = status
        self.role = role

        # Automatically create a default UserInfo instance
        self.user_info = UserInfo()

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
    
class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=True, default='')
    last_name = db.Column(db.String(100), nullable=True, default='')
    avatar = db.Column(db.String(200), nullable=True, default='default.jpg')
    date_of_birth = db.Column(db.Date, nullable=True)
    address = db.Column(db.String(200), nullable=True, default='')
    phone_number = db.Column(db.String(20), nullable=True, default='')
    
    # Foreign key to User model
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)



# Class table
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer,nullable=False)
    section = db.Column(db.String(100), nullable=False)
    group = db.Column(db.Integer,nullable=False)
    students = db.relationship('Student', backref='class_info', lazy=True)
    teacher_classes = db.relationship('TeacherClass', backref='class_info', lazy=True)
    supervisor_classes = db.relationship('SupervisorClass', backref='class_info', lazy=True)

# Association table for Teacher-Class (Many-to-Many relationship)
class TeacherClass(db.Model):
    __tablename__ = 'teacherclass'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)

# Association table for Supervisor-Class (Many-to-Many relationship)
class SupervisorClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)

# Student table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    attendance = db.relationship('Attendance', backref='student_info', lazy=True)

# Attendance table
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    teacher_class_id = db.Column(db.Integer, db.ForeignKey('teacherclass.id'), nullable=False)
    status = db.Column(db.String(10), nullable=False)  # Present, Absent, Late, Excused
    recorded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)