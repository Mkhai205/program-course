from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Program(db.Model):
    __tablename__ = 'programs'

    id = db.Column(db.Integer, primary_key=True)
    program_code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')

    program_courses = db.relationship('ProgramCourse', back_populates='program',
                                       cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Program {self.program_code}>'


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    credits = db.Column(db.Integer, nullable=False, default=3)
    category = db.Column(db.String(100), default='')
    is_required = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text, default='')

    program_courses = db.relationship('ProgramCourse', back_populates='course',
                                       cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Course {self.course_code}>'


class ProgramCourse(db.Model):
    __tablename__ = 'program_courses'

    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    semester = db.Column(db.Integer, nullable=False, default=1)
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    program = db.relationship('Program', back_populates='program_courses')
    course = db.relationship('Course', back_populates='program_courses')

    __table_args__ = (
        db.UniqueConstraint('program_id', 'course_id', name='uq_program_course'),
    )

    def __repr__(self):
        return f'<ProgramCourse program={self.program_id} course={self.course_id}>'
