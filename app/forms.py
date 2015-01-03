from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp, Email, ValidationError
from models import User


class UsernameValidation(object):
    """
    Validates that a username is not already in use when registering or editing information.

    :param message:
        Error message to raise in case of a validation error.
    """
    def __init__(self, message=None):
        if not message:
            message = u'That username is already in use.'
            self.message = message

    def __call__(self, form, field):
        username = User.query.filter_by(username=field.data).first()
        if username is not None:
            raise ValidationError(self.message)


class EmailValidation(object):
    """
    Validates that an email is not already in use when registering or editing information.

    :param message:
        Error message to raise in case of a validation error.
    """
    def __init__(self, message=None):
        if not message:
            message = u'That email is already in use.'
            self.message = message

    def __call__(self, form, field):
        email = User.query.filter_by(email=field.data).first()
        if email is not None:
            raise ValidationError(self.message)


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegistrationForm(Form):
    username = StringField('username', validators=[
        DataRequired(),
        Length(min=3, max=20, message="Your username must be 3-20 characters in length"),
        Regexp(r'^[a-zA-Z0-9-]+$', message="Your username may only contain alphanumeric characters and hyphens"),
        UsernameValidation()
    ])
    email = StringField('email', validators=[
        DataRequired(),
        Email(message="Please enter a valid email address"),
        EmailValidation()
    ])
    password = PasswordField('password', validators=[
        DataRequired(),
        Length(min=8, message="Your password must be at least 8 characters long")
        # TODO - implement password validation regex
    ])


class PostForm(Form):
    title = StringField('title', validators=[DataRequired()])
    post = TextAreaField('post', validators=[DataRequired()])