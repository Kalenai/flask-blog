from flask.ext.wtf import Form
from wtforms import BooleanField, PasswordField, RadioField, StringField, TextAreaField
from wtforms.validators import Email, DataRequired, Length, Regexp,  ValidationError
from models import User


class UsernameEmailValidation(object):
    """
    Validates that a username or email is not already in use when registering or editing information.

    :param message:
        Error message to raise in case of a validation error.
    """
    def __init__(self, message=None):
        if not message:
            message = u'That username or email is already in use'
        self.message = message

    def __call__(self, form, field):
        if field.id is 'username':
            username = User.query.filter_by(username=field.data).first()
            if username is not None:
                raise ValidationError(self.message)
        elif field.id is 'email':
            email = User.query.filter_by(email=field.data).first()
            if email is not None:
                raise ValidationError(self.message)


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegistrationForm(Form):
    username = StringField('username', validators=[
        DataRequired(),
        Length(min=3, max=20, message="Your username must be 3-20 characters in length"),
        Regexp(r'^[a-zA-Z0-9-]+$', message="Your username may only contain alphanumeric characters and hyphens"),
        UsernameEmailValidation(message="That username is already in use")
    ])
    email = StringField('email', validators=[
        DataRequired(),
        Email(message="Please enter a valid email address"),
        UsernameEmailValidation("That email is already in use")
    ])
    password = PasswordField('password', validators=[
        DataRequired(),
        Length(min=8, message="Your password must be at least 8 characters long")
        # TODO - implement password validation regex
    ])


class SettingsForm(RegistrationForm):
    about = TextAreaField('about', validators=[
        Length(max=1000, message="You must keep your 'About Me' section under 1000 characters")
    ])
    location = StringField('location', validators=[
        Length(max=100, message="You must keep your 'Location' section under 100 characters")
    ])
    gender = RadioField('gender', choices=[
        ('m', 'Male'), ('f', 'Female'), ('u', 'Unspecified')
    ])


class PostForm(Form):
    title = StringField('title', validators=[DataRequired()])
    post = TextAreaField('post', validators=[DataRequired()])