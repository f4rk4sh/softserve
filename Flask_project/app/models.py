import jwt
from time import time
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

interviews = db.Table('interviews', db.Model.metadata,
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('interview_id', db.Integer, db.ForeignKey('interview.id')))

sets = db.Table('sets', db.Model.metadata,
                db.Column('interview_id', db.Integer, db.ForeignKey('interview.id')),
                db.Column('set_id', db.Integer, db.ForeignKey('set.id')))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    is_recruiter = db.Column(db.Boolean, default=False)
    grades = db.relationship('Grade', backref='evaluator', cascade='all, delete-orphan', lazy='dynamic')
    interviews = db.relationship('Interview', secondary=interviews)

    def __repr__(self):
        return f'<User {self.id}>'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_set_password_token(self, expires_in=7200):
        return jwt.encode({'set_password': self.id, 'exp': time() + expires_in},
                          current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_set_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['set_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interviewee = db.Column(db.String(50))
    date = db.Column(db.DateTime)
    score = db.Column(db.Integer)
    sets = db.relationship('Set', secondary=sets)

    def __repr__(self):
        return f'<Interview {self.id}>'

    def __str__(self):
        return self.interviewee


class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    area = db.Column(db.String(100))
    level = db.Column(db.String(50))
    questions = db.relationship('Question', backref='set', cascade='all, delete-orphan', lazy='dynamic')

    def __repr__(self):
        return f'<Set {self.id}>'

    def __str__(self):
        return self.title


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200))
    answer = db.Column(db.String(400))
    max_grade = db.Column(db.Integer)
    set_id = db.Column(db.Integer, db.ForeignKey('set.id'))
    grades = db.relationship('Grade', backref='question', cascade='all, delete-orphan', lazy='dynamic')

    def __repr__(self):
        return f'<Question {self.id}>'

    def __str__(self):
        return f'{self.question[:9]}...'


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Integer)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Grade {self.id}>'

    def __str__(self):
        return self.grade
