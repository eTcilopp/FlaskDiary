from flask import Blueprint, request
from flask_restful import Resource, reqparse
from .models import BlogPosts, Comments
from sqlalchemy import not_, exists, and_
from . import db


rest_api = Blueprint('rest_api_bp', __name__, url_prefix='/api')


@rest_api.route('/uncommented_posts')
def uncommented_posts():
    ai_user_id = 2

    # Subquery to find BlogPosts ids that have comments from the given user
    subquery = db.session.query(Comments.parent_post_id).\
        filter(Comments.author_id == ai_user_id).\
        subquery()
    # Query to find BlogPosts that do not have comments from the given user
    posts_without_user_comments = db.session.query(BlogPosts).\
        filter(~exists().where(BlogPosts.id == subquery.c.parent_post_id)).\
        all()
    # posts_without_comments = db.session.query(BlogPosts).all()
    res = list()
    for post in posts_without_user_comments:
        res.append({'author_id': post.author_id, 'created': post.created, 'modified': post.modified, 'text': post.text})

    return {'uncommented_posts': res}


'''
def uncommented_posts():
    ai_user_id = 2
    if request.method == 'POST':
        return {'message': f'Hello, World ! POST {request.headers}'}

'''

@rest_api.route('/uncommented_comments')
def uncommented_comments():
    ai_user_id = 2

    replied_comment_ids = db.session.query(Comments.parent_comment_id).\
        filter(Comments.author_id == ai_user_id).\
        subquery()

    # Main query to find comments that:
    # - Have a parent comment created by the given user
    # - Do not have replies from the given user
    comments_without_replies_from_user = db.session.query(Comments).\
        join(Comments, Comments.id == Comments.parent_comment_id).\
        filter(Comments.parent_comment_id is not None,  # Ensure the comment has a parent
            Comments.author_id != ai_user_id,  # The comment is not by the given user
            Comments.parent_comment_id == Comments.id,  # Join condition to match parent comment
            Comments.author_id == ai_user_id,  # Parent comment is created by the given user
            ~exists().where(and_(  # Ensure no replies from the given user to this comment
                Comments.id == replied_comment_ids.c.parent_comment_id,
                Comments.author_id == ai_user_id
            ))).\
        all()
    res = list()
    for comment in comments_without_replies_from_user:
        res.append({'author_id': comment.author_id, 'created': comment.created, 'modified': comment.modified, 'text': comment.text})

    return {'uncommented_comments': res}

