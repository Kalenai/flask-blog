from flask import render_template, g, redirect, url_for, session, request, flash
from flask.ext.login import login_user, logout_user, current_user
from app import app, db, login_manager
from models import User, Post
from forms import LoginForm, PostForm, RegistrationForm
from utilities import flash_errors

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html'
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = User.query.filter_by(username=form.username.data).first()
        if not username or not username.verify_password(form.password.data):
            flash("That username and password combination do not match our records.  Please try again.")
        else:
            login_user(username)
            flash("Logged in successfully.  Welcome, %s!" % username.username)
            return redirect(url_for('index'))
    else:
        flash_errors(form)
    return render_template(
        'login.html',
        form=form
    )

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
        )
        new_user.hash_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        flash_errors(form)
    return render_template(
        'register.html',
        form=form
    )

@app.route('/post', methods=['GET', 'POST'])
def post():
    form = PostForm()
    return render_template(
        'post.html',
        form=form
    )