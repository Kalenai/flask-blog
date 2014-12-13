from app import db
from passlib.apps import custom_app_context as pwd_context

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(100), unique=True)
    about = db.Column(db.Text(1200))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password, scheme="sha512_crypt")

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    post_body = db.Column(db.Text(4000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % self.post_body