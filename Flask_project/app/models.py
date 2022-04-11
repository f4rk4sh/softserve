import jwt
from time import time
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

user_interview = db.Table('user_interview', db.Model.metadata,
                          db.Column('id', db.Integer, primary_key=True),
                          db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                          db.Column('interview_id', db.Integer, db.ForeignKey('interview.id')))

interview_set = db.Table('interview_set', db.Model.metadata,
                         db.Column('id', db.Integer, primary_key=True),
                         db.Column('interview_id', db.Integer, db.ForeignKey('interview.id')),
                         db.Column('set_id', db.Integer, db.ForeignKey('set.id')))

interview_question = db.Table('interview_question', db.Model.metadata,
                              db.Column('id', db.Integer, primary_key=True),
                              db.Column('interview_id', db.Integer, db.ForeignKey('interview.id')),
                              db.Column('question_id', db.Integer, db.ForeignKey('question.id')))

question_set = db.Table('question_set', db.Model.metadata,
                        db.Column('id', db.Integer, primary_key=True),
                        db.Column('question_id', db.Integer, db.ForeignKey('question.id')),
                        db.Column('set_id', db.Integer, db.ForeignKey('set.id')))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    is_recruiter = db.Column(db.Boolean, default=False)
    interviews = db.relationship('Interview', secondary=user_interview, back_populates='users')
    grades = db.relationship('Grade', backref='evaluators', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.id}>'

    def __str__(self):
        return f'{self.name}'

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
    brief = db.Column(db.Text)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    score = db.Column(db.Integer)
    users = db.relationship('User', secondary=user_interview, back_populates='interviews')
    sets = db.relationship('Set', secondary=interview_set, back_populates='interviews')
    questions = db.relationship('Question', secondary=interview_question, back_populates='interviews')
    grades = db.relationship('Grade', backref='interviews', lazy='dynamic')

    def __repr__(self):
        return f'<Interview {self.id}>'

    def __str__(self):
        return self.interviewee


class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    area = db.Column(db.String(50))
    level = db.Column(db.String(50))
    interviews = db.relationship('Interview', secondary=interview_set, back_populates='sets')
    questions = db.relationship('Question', secondary=question_set, back_populates='sets')

    def __repr__(self):
        return f'<Set {self.id}>'

    def __str__(self):
        return self.title


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(50))
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    max_grade = db.Column(db.Integer)
    interviews = db.relationship('Interview', secondary=interview_question, back_populates='questions')
    sets = db.relationship('Set', secondary=question_set, back_populates='questions')
    grades = db.relationship('Grade', backref='questions', lazy='dynamic')

    def __repr__(self):
        return f'<Question {self.id}>'

    def __str__(self):
        return f'{self.question}'


class Grade(db.Model):

    __table_args__ = (db.PrimaryKeyConstraint('user_id', 'interview_id', 'question_id'),)

    grade = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    interview_id = db.Column(db.Integer, db.ForeignKey('interview.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    def __repr__(self):
        return f'<Grade {self.id}>'

    def __str__(self):
        return self.grade
