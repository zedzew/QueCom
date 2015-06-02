from flask import g
from flask.ext.login import current_user
from wtforms import StringField, PasswordField, validators, TextAreaField
from wtforms.validators import Regexp
from flask.ext.wtf import Form
from app import app


class QuestionForm(Form):
    question = StringField('Question', validators=[validators.required()])

class LoginForm(Form):
    name = StringField('Name', validators=[validators.Length(5, 64),
                                                    Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
                                                    0,'Username must have only letteres,'
                                                    'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[validators.DataRequired()])


class CommentForm(Form):
    comment = TextAreaField('Comment', validators=[validators.required()])


@app.before_request
def before_request():
    g.user = current_user
