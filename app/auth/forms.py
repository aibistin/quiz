# app/auth/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField,  BooleanField, SubmitField
from wtforms import TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.validators import Length
# Commmunicate logins with the db
from app.models import User


# ------------------------------------------------------------------------------
#    Login Forms
# ------------------------------------------------------------------------------

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Start Assessment')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(
                'This email exists already. Please use a different email address.')


# ------------------------------------------------------------------------------
#    User Profile Forms
# ------------------------------------------------------------------------------


# class EditProfileForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     about_me = StringField('About Me', validators=[Length(min=0, max=140)])
#     submit = SubmitField('Submit')

#     def __init__(self, original_username, *args, **kwargs):
#         super(EditProfileForm, self).__init__(*args, **kwargs)
#         self.original_username = original_username

#     def validate_username(self, username):
#         if username.data != self.original_username:
#             user = User.query.filter_by(username=self.username.data).first()
#             if user is not None:
#                 raise ValidationError(
#                     "Drat! Username exists already. Pick another one!")


# class ResetPasswordRequestForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     submit = SubmitField('Request Password Reset')


# class ResetPasswordForm(FlaskForm):
#     password = PasswordField('Password', validators=[DataRequired()])
#     password2 = PasswordField('Repeat Password', validators=[
#                              DataRequired(), EqualTo('password')])
#     submit = SubmitField('Reset Password')


# ------------------------------------------------------------------------------
#    Other Forms
# ------------------------------------------------------------------------------


# class MessageForm(FlaskForm):
#     message = TextAreaField('Text Msg:', validators=[
#         DataRequired(), Length(min=1, max=140)])
#     submit = SubmitField('Send')


# class EmptyForm(FlaskForm):
#     submit = SubmitField('Submit')
