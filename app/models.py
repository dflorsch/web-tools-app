from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(UserMixin, db.Model, Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    e_mail = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Project(db.Model, Base):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    agency = db.Column(db.String(255))
    customer = db.Column(db.String(255))
    project_name = db.Column(db.String(255))
    project_role = db.Column(db.String(255))
    hourly_rate = db.Column(db.Integer)
    planned_hours = db.Column(db.Integer)
    project_start = db.Column(db.Date)
    project_end = db.Column(db.Date)
    competence_center = db.Column(db.String(255))
    mentoring_group = db.Column(db.String(255))
    project_extension = db.Column(db.Boolean)
    note = db.Column(db.String(255))

    def __repr__(self):
        return f'<Project {self.project_name}>'


class Attendance(db.Model, Base):
    __tablename__ = 'attendances'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    note = db.Column(db.String(255))

    user = db.relationship('User', backref=db.backref('attendances', lazy=True))

    def __repr__(self):
        return f'<Attendance {self.id}>'
