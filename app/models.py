# app/models.py
import base64
import os
from datetime import datetime, timedelta
from time import time
from hashlib import md5
from flask import current_app,  redirect, request, url_for
# from flask_login import UserMixin
# from app import create_app, db, login
from app import db
from functools import wraps
from werkzeug.security import safe_str_cmp


# Associative or bridging table
user_questions = db.Table('user_questions',
                          db.Column('user_id', db.Integer,
                                    db.ForeignKey('user.id')),
                          db.Column('question_id', db.Integer,
                                    db.ForeignKey('question.id')),
                          db.Column('is_correct', db.Boolean,
                                    nullable=False, default=0),
                          db.UniqueConstraint(
                              'user_id', 'question_id', name='user_question_uix_1')
                          )


# ------------------------------------------------------------------------------
# Mixin - Paginate the API responses
# ------------------------------------------------------------------------------
class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            'data': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


# class User(PaginatedAPIMixin, UserMixin, db.Model):
class User(PaginatedAPIMixin,  db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64),  nullable=False, unique=False)
    last_name = db.Column(db.String(64),  nullable=False, unique=False)
    email = db.Column(db.String(120), index=True, nullable=False, unique=True)
    #
    # last_seen = db.Column(db.DateTime, default=datetime.utcnow())
    token = db.Column(db.String(120), index=True, nullable=False, unique=True)
    token_expire_time = db.Column(db.DateTime, index=True, nullable=False)
    created = db.Column(db.DateTime, index=True,
                        nullable=False, default=datetime.utcnow())

    asked = db.relationship(
        'Question', secondary=user_questions,
        backref=db.backref('user', lazy='dynamic'), lazy='dynamic')

    # answered = db.relationship(
    #     'User', secondary=answers,
    #     primaryjoin=(answers.c.answer_id == id),
    #     secondaryjoin=(answers.c.answered_id == id),
    #     backref=db.backref('answers', lazy='dynamic'), lazy='dynamic')

    # def answered_questions(self):
    #     answered = Question.query.join(
    #         answers, (answers.c.answered_id == Question.user_id)).filter(
    #             answers.c.answer_id == self.id)
    #     own = Question.query.filter_by(user_id=self.id)
    #     return answered.union(own).order_by(Question.timestamp.desc())

    # def asked_questions(self):
    #     answered = Question.query.join(
    #         answers, (answers.c.answered_id == Question.user_id)).filter(
    #             answers.c.answer_id == self.id)
    #     own = Question.query.filter_by(user_id=self.id)
    #     return answered.union(own).order_by(Question.timestamp.desc())

    def create_reset_user_token(self, expires_in=600):
        current_app.logger.debug(
            "[create_reset_user_token] User Email: " + str(self.email))

        if not self.token:
            self.token = base64.b64encode(os.urandom(24)).decode('utf-8')

        self.token_expire_time = datetime.utcnow() + timedelta(seconds=expires_in)
        if expires_in <= 0:
            return None
        return self.token

    def remove_user_token(self):
        self.create_reset_user_token(-1)

    def username(self):
        return self.first_name + ' ' + self.last_name

    @staticmethod
    def verify_user_token(token):
        current_app.logger.debug(
            "[verify_user_token] ###### Verify WEB Token ###### : " + token)
        current_user = User.query.filter_by(token=token).first()
        if not current_user or current_user.token_expire_time <= datetime.utcnow():
            return None
        return current_user

    def to_dict(self):
        delta_time = datetime.utcnow() - self.created
        remaining_time = self.token_expire_time - datetime.utcnow()

        data = {
            'id': self.id,
            'username': self.first_name + ' ' + self.last_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'token': self.token,
            'token_expire_time': self.token_expire_time.isoformat() + 'Z' if self.token_expire_time else None,
            'delta_time_seconds':  int(delta_time.total_seconds()),
            'remaining_time_seconds': int(remaining_time.total_seconds()),
            'question_count':  self.asked.count() if self.asked else [],
            'questions': ([question.to_dict() for question in self.asked.all()]),
            '_links': {
                # 'answered': url_for('get_answered', id=self.id),
            }
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['first_name', 'last_name', 'email']:
            if field in data:
                setattr(self, field, data[field])

        setattr(self, 'token', self.create_reset_user_token())

    def __repr__(self):
        return '<UserName: {0} Email: {1}>'.format(self.first_name + ' ' + self.last_name, self.email)


# @login.user_loader
# def load_user(id):
#     print("******* ############# [load_user'] Loading User ID: " + str(id))
#     return User.query.get(int(id))

# ------------------------------------------------------------------------------
# Decorator for verifying the Token
# ------------------------------------------------------------------------------


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        current_app.logger.debug("[token_required] Path: " + request.path)
        current_app.logger.debug("[token_required] Data: ")
        data = request.get_json() or {}
        current_app.logger.debug(data)

        if 'user_token' in request.view_args:
            current_user_token = request.view_args['user_token']

        current_user_token = request.view_args['user_token'] if 'user_token' in request.view_args else None

        if not current_user_token:
            current_app.logger.debug("[token_required] No Token -> Register")
            return redirect(url_for('auth.register'), code=307)

        current_user = User.verify_user_token(current_user_token)

        if current_user is None:
            current_app.logger.error(
                "[token_required] No user for token -> Register")
            current_app.logger.error("[token_required] " + current_user_token)
            return redirect(url_for('auth.register'))

        current_app.logger.debug(
            "[token_required] Current User: " + current_user.username())

        return f(current_user)

    return decorated
# ------------------------------------------------------------------------------
#  Question Class
# ------------------------------------------------------------------------------

# AnsweredText	"10"
# ChildQuestionAnsweredText	null
# ChildQuestionAnsweredText2	null
# OptionId	null
# QuestionId	2474384


class Question(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(240),  unique=True, nullable=False)
    answer = db.Column(db.String(60),  unique=False, nullable=False)
    options = db.relationship('Option', backref='question', lazy='dynamic')
    files = db.relationship('File', backref='question', lazy='dynamic')

    def to_dict(self):
        data = {
            'id': self.id,
            'body': self.body,
            'answer': self.answer,
            'options': ([option.to_dict() for option in self.options.all()]),
            'files': ([file.to_dict() for file in self.files.all()]),
        }
        return data

    def __repr__(self):
        return '<Question id: {0}, body: {1}, answer: {2}>'.format(self.id, self.body, self.answer)


# ------------------------------------------------------------------------------
#  Option Class
# ------------------------------------------------------------------------------

# AnsweredText	"10"
# ChildQuestionAnsweredText	null
# ChildQuestionAnsweredText2	null
# OptionId	null
# QuestionId	2474384

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(240),  unique=False, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    is_answer = db.Column(db.Boolean, default=0)
    db.UniqueConstraint('body', 'question_id', name='question_option_uix_1')

    def to_dict(self):
        data = {
            'id': self.id,
            'body': self.body,
            'question_id': self.question_id,
        }
        return data

    def __repr__(self):
        return '<Option id: {0}, body: {1}, question_id: {2}, is_answer: {3}>'.format(self.id, self.body, self.question_id, self.is_answer)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(240),  unique=False, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    db.UniqueConstraint('location', 'question_id', name='file_location_uix_1')

    def to_dict(self):
        data = {
            'id': self.id,
            'location': self.location,
            'question_id': self.question_id,
        }
        return data

    def __repr__(self):
        return '<File id: {0}, location: {1}, question_id: {2}>'.format(self.id, self.location, self.question_id)

# ------------------------------------------------------------------------------
#  Answer Class
# ------------------------------------------------------------------------------

# AnsweredText	"10"
# ChildQuestionAnsweredText	null
# ChildQuestionAnsweredText2	null
# OptionId	null
# QuestionId	2474384

# class Answer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     answer_text = db.Column(db.String(20), index=False, unique=False, nullable=True)
#     question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

#     def __repr__(self):
#         return '<Answer {}>'.format(self.body)
