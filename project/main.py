from flask import Blueprint, render_template, session, request, Flask, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf.csrf import generate_csrf
from .forms import BlogPostForm
from .models import BlogPosts
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/posts')
@login_required
def blog_posts():
    blog_posts = BlogPosts.query.filter(BlogPosts.author_id == current_user.id).order_by(BlogPosts.id.desc()).all()
    print(blog_posts)
    return render_template('blog_posts.html', blog_posts=blog_posts, name=current_user.name)


@main.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        # Process the form data, e.g., save to database
        content = form.content.data
        new_post = BlogPosts(author_id=current_user.id, text=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.blog_posts'))  # Redirect to another page after processing
    return render_template('create_post.html', form=form)


# @main.route('/submit_post', methods=['POST'])
# @login_required
# def submit_post():
#     data = request.json
#     print(data)
#     # Here, you would normally process the form data
#     # Since we're doing nothing for now, we'll skip straight to rendering the profile page
    
#     return render_template('blog_posts.html')
