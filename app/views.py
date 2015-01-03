from flask import render_template, g, redirect, url_for, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from models import User, Post
from forms import LoginForm, PostForm, RegistrationForm
from utilities import flash_errors
from datetime import datetime
from config import POSTS_PER_PAGE


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(401)
def forbidden_error(error):
    return render_template(
        '401.html',
    ), 401


@app.errorhandler(403)
def forbidden_error(error):
    return render_template(
        '403.html',
    ), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template(
        '404.html',
    ), 404


@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template(
        '500.html',
    ), 500


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
        # TODO - make username matching case-insensitive
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
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            timestamp=datetime.utcnow(),
            title=form.title.data,
            post_body=form.post.data,
            author=g.user
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Your post was successfully submitted!')
        return redirect(url_for('user', username=g.user.username))
    else:
        flash_errors(form)
    return render_template(
        'post.html',
        form=form
    )


@app.route('/user/<username>')
@app.route('/user/<username>/<int:page>')
def user(username, page=1):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash_errors(
            'The user %s is not found.  Ensure you typed the username correctly and try again.' % user
        )
        return redirect(url_for('index'))
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template(
        'user.html',
        user=user,
        posts=posts
    )

@app.route('/settings')
@login_required
def settings():
    pass  # TODO - Implement user settings.  Maybe with different tabs?