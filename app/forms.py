from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp, Email

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class RegistrationForm(Form):
    username = StringField('username', validators=[
        DataRequired(),
        Length(min=3, max=15, message="Your username must be 3-15 characters in length"),
        Regexp(r'^[a-z0-9_-]$',
               message="Your username may only contain alphanumeric characters, underscores, and hyphens")
    ])
    email = StringField('email', validators=[
        DataRequired(),
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('password', validators=[
        DataRequired(),
        Length(min=12, message="Your password must be at least 12 characters long")
        # TODO - implement password validation regex
    ])

class PostForm(Form):
    title = StringField('title', validators=[DataRequired()])
    post = TextAreaField('post', validators=[DataRequired()])