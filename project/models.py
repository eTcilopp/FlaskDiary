from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class BlogPosts(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Assuming your users table is named 'users'
    created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    text = db.Column(db.Text)

