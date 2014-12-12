from flask import render_template
from app import app
from forms import LoginForm, PostForm

@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html'
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template(
        'login.html',
        form = form
    )

@app.route('/post', methods=['GET', 'POST'])
def post():
    form = PostForm()
    return render_template(
        'post.html',
        form = form
    )