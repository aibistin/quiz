# app/models.py
import base64
import os
from datetime import datetime, timedelta
from time import time
from hashlib import md5
from flask import current_app,  redirect, request, url_for
from app import db
from functools import wraps
from urllib.parse import quote, unquote
from werkzeug.security import safe_str_cmp


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64),  nullable=False, unique=False)
    last_name = db.Column(db.String(64),  nullable=False, unique=False)
    email = db.Column(db.String(120), index=True, nullable=False, unique=True)
    token = db.Column(db.String(120), index=True, nullable=False, unique=True)
    token_expire_time = db.Column(db.DateTime, index=True, nullable=False)
    created = db.Column(db.DateTime, index=True,
                        nullable=False, default=datetime.utcnow())
    questions = db.relationship("UserQuestion", backref="user", lazy='dynamic')

    def last_answered_question_id(self):
        last_answered = (self.questions.filter_by(is_answered=True).order_by(
            UserQuestion.question_id.desc())).first()
        return last_answered.question_id if last_answered else None

    def get_last_unanswered_question_id(self):
        last_unanswered_user_question = (self.questions.filter_by(is_answered=False).order_by(
            UserQuestion.question_id.desc())).first()
        return last_unanswered_user_question.question_id if last_unanswered_user_question else None


    def get_next_question(self):
        next_question = None
        last_unanswered_user_question = (self.questions.filter_by(is_answered=False).order_by(
            UserQuestion.question_id.desc())).first()

        current_app.logger.debug("[get_next_question] last_unanswered_user_question")
        current_app.logger.debug(last_unanswered_user_question)

        if last_unanswered_user_question:
            next_question = db.session.query(Question).filter(
                Question.id == last_unanswered_user_question.question_id).first()
        else:
            last_answered_id = self.last_answered_question_id() or 0
            next_question = db.session.query(Question).filter(Question.id > last_answered_id ).order_by(Question.id).first()

        return next_question

    #    Answer 
    # AnsweredText	null
    # ChildQuestionAnsweredText	null
    # ChildQuestionAnsweredText2	null
    # OptionId	"11427870"
    # QuestionId	2474351

    def save_the_answer_to_db(self, answer_data):
        answer = None
        is_correct = False
        answered_question = Question.query.filter_by(
            id=answer_data["QuestionId"]).first()
        current_app.logger.debug("Answered Question")
        current_app.logger.debug(answered_question)

        user_question_asked  =  self.questions.filter_by(question_id=answer_data["QuestionId"]).first()
        if user_question_asked is None:
            #TODO Throw an error!
            current_app.logger.error("[save_the_answer_to_db] ERROR! You must ask a question before answering it!")
            return

        current_app.logger.debug("[save_the_answer_to_db] Asked UserQuestion")
        current_app.logger.debug(user_question_asked)

        current_app.logger.debug("[save_the_answer_to_db] Users Answer")
        current_app.logger.debug(answer_data)

        if answer_data["OptionId"] is not None:
            option = answered_question.options.filter(
                Option.id == answer_data["OptionId"]).first()
            # TODO use this or the user_question.is_correct field
            if option is None: 
                current_app.logger.error("ERROR: That option, " + answer_data["OptionId"]+ ", doesn't exist for this question!")
            else:
                answer = option.body
        elif answer_data["AnsweredText"] is not None:
            answer = answer_data["AnsweredText"]
        elif answer_data["ChildQuestionAnsweredText"] is not None:
            answer = answer_data["ChildQuestionAnsweredText"]
        elif answer_data["ChildQuestionAnsweredText2"] is not None:
            answer = answer_data["ChildQuestionAnsweredText2"]
        else:
            # TODO resubmit the question, or throw an error?
            current_app.logger.error("You must answer the question")

        if str(answer) == str(answered_question.answer):
            is_correct = True

        user_question_asked.is_answered = True
        user_question_asked.is_correct = is_correct
        db.session.commit()


    def save_the_question_to_db(self, question_id):
        asked_question = Question.query.filter_by(id=question_id).first()
        current_app.logger.debug("[save_the_question_to_db] Asked Question")
        current_app.logger.debug(asked_question)

        # Check if it already exists first
        user_question  =  self.questions.filter_by(question_id=asked_question.id).first()
        current_app.logger.debug("[save_the_question_to_db] Existing User Question")
        current_app.logger.debug(user_question)

        if not user_question:
            user_question = UserQuestion(user_id=self.id, question_id=asked_question.id,
                              is_answered=False, is_correct=False)
            db.session.add(user_question)
            db.session.commit()
            current_app.logger.debug("[save_the_question_to_db] New User Question")
            current_app.logger.debug(user_question)

        return user_question

    def create_reset_token(self, expires_in=3600):
        if not self.token:
            self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expire_time = datetime.utcnow() + timedelta(seconds=expires_in)
        if expires_in <= 0:
            return None
        return self.token

    def remove_token(self):
        self.create_reset_token(-1)

    def get_quoted_token(self):
        return quote(self.token, safe='')

    def username(self):
        return self.first_name + ' ' + self.last_name

    @ staticmethod
    def verify_user_token(token):
        token = unquote(token)
        current_app.logger.debug("[verify_user_token] Token: " + token)
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
            # 'question_count':  self.asked.count() if self.asked else [],
            # 'questions': ([question.to_dict() for question in self.asked.all()]),
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['first_name', 'last_name', 'email']:
            if field in data:
                setattr(self, field, data[field])

        setattr(self, 'token', self.create_reset_token())

    def __repr__(self):
        return '<UserName: {0} Email: {1}>'.format(self.first_name + ' ' + self.last_name, self.email)


# ------------------------------------------------------------------------------
# Decorator for verifying the Token
# ------------------------------------------------------------------------------


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        current_app.logger.debug("[token_required] Path: " + request.path)

        if 'user_token' in request.view_args:
            current_user_token = request.view_args['user_token']

        current_user_token = request.view_args['user_token'] if 'user_token' in request.view_args else None

        if not current_user_token:
            current_app.logger.debug("[token_required] No Token -> Register")
            return redirect(url_for('auth.register'), code=307)

        current_user = User.verify_user_token(current_user_token)

        if current_user is None:
            current_app.logger.debug(
                "[token_required] No user for token -> Register")
            current_app.logger.debug(
                "[token_required] Token: " + current_user_token)
            return redirect(url_for('auth.register'))

        current_app.logger.debug(
            "[token_required] User: " + current_user.username())

        return f(current_user)

    return decorated
# ------------------------------------------------------------------------------
#  Question Class
# ------------------------------------------------------------------------------


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(240),  unique=True, nullable=False)
    answer = db.Column(db.String(60),  unique=False, nullable=False)
    options = db.relationship('Option', backref='question', lazy='dynamic')
    files = db.relationship('File', backref='question', lazy='dynamic')
    users = db.relationship("UserQuestion", backref="question", lazy='dynamic')

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
#  Bridging Table Between User and their Questions
# ------------------------------------------------------------------------------

class UserQuestion(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.id'), primary_key=True)
    is_answered = db.Column(db.Boolean, nullable=False, default=0)
    is_correct = db.Column(db.Boolean, nullable=False, default=0)
    db.UniqueConstraint('user_id', 'question_id', name='user_question_uix_1')
    users = db.relationship("User", backref="question")
    questions = db.relationship("Question", backref="user")

    def answered_already(self, user_id=99):
        current_app.logger.debug("[answered_already] User Id: " + str(user_id))
        return self.query.filter_by(user_id=user_id, is_answered=1).order_by(self.question_id)

    def to_dict(self):
        data = {
            'user_id': self.user_id,
            'question_id': self.question_id,
            'is_answered': self.is_answered,
            'is_correct': self.is_correct,
        }
        return data

    def __repr__(self):
        return '<UserQuestion user_id: {0}, question_id: {1}, is_answered: {2}, is_correct: {2}>'.format(self.user_id, self.question_id, self.is_correct)
# ------------------------------------------------------------------------------
#  Option Class
# ------------------------------------------------------------------------------


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
            'is_answer': self.is_answer,
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
