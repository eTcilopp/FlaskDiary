from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .forms import BlogPostForm, CommentForm
from .models import BlogPosts, Comments
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/posts')
@login_required
def blog_posts():
    blog_posts = BlogPosts.query.filter(BlogPosts.author_id == current_user.id).order_by(BlogPosts.id.desc()).all()
    return render_template('blog_posts.html', blog_posts=blog_posts, name=current_user.name)


def get_comments_with_children(comments, children_comment_lst=None, level=1):
    if children_comment_lst is None:
        children_comment_lst = []
    for comment in comments:
        comment.level = level
        children_comment_lst.append(comment)
        children_comments = Comments.query.filter_by(parent_comment_id=comment.id).order_by(Comments.id.desc()).all()

        get_comments_with_children(children_comments, children_comment_lst, level + 1)

    return children_comment_lst


@main.route('/individual_posts/<int:post_id>', methods=['GET', 'POST'])
@login_required
def individual_post(post_id):
    form = CommentForm()
    individual_post = BlogPosts.query.filter(BlogPosts.author_id == current_user.id).filter(BlogPosts.id == post_id).first()
    comments = Comments.query.filter(Comments.parent_post_id == post_id).order_by(Comments.id.asc()).all()
    comments_with_children = get_comments_with_children(comments)

    if form.validate_on_submit():
        content = form.content.data
        comment_id = request.form.get('comment_id')
        if comment_id:
            new_comment = Comments(author_id=current_user.id, parent_comment_id=comment_id, text=content)
        else:
            new_comment = Comments(author_id=current_user.id, parent_post_id=post_id, text=content)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('main.individual_post', post_id=post_id))
    return render_template('individual_post.html', post=individual_post, form=form, comments=comments_with_children, name=current_user.name)


@main.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        content = form.content.data
        new_post = BlogPosts(author_id=current_user.id, text=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.blog_posts'))
    return render_template('create_post.html', form=form)
