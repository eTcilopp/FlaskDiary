from flask_login import UserMixin
from sqlalchemy import CheckConstraint
import enum
from . import db

class PostStatusEnum(enum.Enum):
    published = 'pub'
    deleted = 'del'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))
    name = db.Column(db.String(100))


class BlogPosts(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', backref='posts')
    created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    modified = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    status = db.Column(db.Enum(PostStatusEnum), default=PostStatusEnum.published, nullable=False)
    text = db.Column(db.Text)


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', backref='comments')
    parent_post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=True)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    modified = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    status = db.Column(db.Enum(PostStatusEnum), default=PostStatusEnum.published, nullable=False)
    text = db.Column(db.Text)

    check_constraint = CheckConstraint("parent_post_id IS NOT NULL OR parent_comment_id IS NOT NULL")
    __table_args__ = (check_constraint,)
