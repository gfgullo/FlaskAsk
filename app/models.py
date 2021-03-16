from app import db
from flask import current_app, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime as dt


class User(UserMixin, db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    questions = db.relationship('Question', backref='author', lazy='dynamic')
    answers = db.relationship('Answer', backref='author', lazy='dynamic')
    upvotes = db.relationship('Upvote', foreign_keys='Upvote.user_id', backref='user', lazy='dynamic')


    def to_dict(self):

        user_dict = {
            "username": self.username,
        }


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True


    def upvote(self, question):
        if not self.has_upvoted_question(question):
            upvote = Upvote(user_id = self.id, question_id = question.id)
            db.session.add(upvote)


    def downvote(self, question):
        if self.has_upvoted_question(question):
            Upvote.query.filter_by(user_id=self.id, question_id=question.id).delete()


    def has_upvoted_question(self, question):
        return Upvote.query.filter(
            Upvote.user_id == self.id,
            Upvote.question_id == question.id).count() > 0


class Answer(db.Model):
    __tablename__ = "answers"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=dt.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))


    def to_dict(self):

        answer_dict = {
            "id": self.id,
            'url': url_for('api.get_answer', id=self.id),
            'body': self.body,
            'author_id': self.author_id,
            'question_url': url_for('api.get_question', id=self.question_id)
        }

        return answer_dict


class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, index=True, default=dt.utcnow)

    answers = db.relationship('Answer', backref='question', lazy='dynamic', primaryjoin=id==Answer.question_id, cascade="all, delete")

    correct_answer_id = db.Column(db.Integer, db.ForeignKey('answers.id', name="correct_answer_id"))
    correct_answer = db.relationship('Answer', uselist=False, single_parent=True, lazy="select",
                                     post_update=True, primaryjoin=correct_answer_id==Answer.id,
                                     cascade="all, delete")

    upvotes = db.relationship('Upvote', backref='question', lazy='dynamic')



    def to_dict(self, full=False):

        question_dict = {
            "id": self.id,
            'url': url_for('api.get_question', id=self.id),
            'title': self.title,
            'author_id': self.author_id
        }

        if(full):
            question_dict['body'] = self.body

        return question_dict


class Upvote(db.Model):
    __tablename__ = "upvotes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
