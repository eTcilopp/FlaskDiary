from flask import Blueprint, request
from flask_restful import Resource, reqparse
from .models import BlogPosts, Comments, User
from sqlalchemy import not_, exists, and_
from . import db
import json


rest_api = Blueprint('rest_api_bp', __name__, url_prefix='/api')


@rest_api.route('/posts/<int:start_post_id>')
def new_posts(start_post_id):
    posts = BlogPosts.query.filter(BlogPosts.id > start_post_id).all()
    new_post_lst = list()
    for post in posts:
        new_post_lst.append(
            {
                'external_id': post.id,
                'author_id': post.author_id,
                'created': post.created,
                'modified': post.modified,
                'text': post.text
            })

    return {'new_posts': new_post_lst}


@rest_api.route('/comments/<int:start_comment_id>')
def new_comments(start_comment_id):
    comments = Comments.query.filter(Comments.id > start_comment_id).all()
    new_comment_lst = list()
    for comment in comments:
        new_comment_lst.append(
            {
                'external_id': comment.id,
                'author_id': comment.author_id,
                'parent_post_id': comment.parent_post_id,
                'parent_comment_id': comment.parent_comment_id,
                'created': comment.created,
                'modified': comment.modified,
                'text': comment.text
            })

    return {'new_posts': new_comment_lst}


@rest_api.route('/users/<int:start_user_id>')
def new_users(start_user_id):
    users = User.query.filter(User.id > start_user_id).all()
    new_user_lst = list()
    for user in users:
        new_user_lst.append(
            {
                'external_id': user.id,
                'email': user.email,
                'name': user.name
            })

    return {'new_posts': new_user_lst}


@rest_api.route('/add_comment', methods=['POST'])
def add_comment():
    data = request.data
    data_str = data.decode('utf-8')
    try:
        data_json = json.loads(data_str)
    except json.JSONDecodeError as e:
        return {'error': str(e)}
    Comments(**data_json)
    new_comment = Comments(**data_json)
    db.session.add(new_comment)
    db.session.commit()
    return {'success': new_comment.id}
