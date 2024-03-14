from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm, SignUpForm  
from .models import User
from . import db

auth = Blueprint('auth', __name__)

# @auth.route('/login')
# def login():
#     return render_template('login.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Here, you would check the user's login credentials
        # If successful:
        flash('Login requested for user {}, remember_me={}'.format(
            form.email.data, form.remember.data))
        email = request.form.get('email')
        password = request.form.get('password')

        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.blog_posts'))  # Redirect to a different page as appropriate
    return render_template('login.html', title='Sign In', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()  # if this returns a user, then the email already exists in database

        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Signup requested for email={}, name={}'.format(form.email.data, form.name.data))
        return redirect(url_for('main.blog_posts'))  # Redirect to the index or a confirmation page
    return render_template('signup.html', title='Sign Up', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))