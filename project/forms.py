from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class SignUpForm(FlaskForm):
    email = StringField('Email!', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email", "class": "input is-large", "autofocus": ""})
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)], render_kw={"placeholder": "Name", "class": "input is-large"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)], render_kw={"placeholder": "Password", "class": "input is-large"})


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Your Email", "class": "input is-large", "autofocus": ""})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Your Password", "class": "input is-large"})
    remember = BooleanField('Remember Me')


class BlogPostForm(FlaskForm):
    content = HiddenField('Content', validators=[DataRequired()])


class CommentForm(FlaskForm):
    content = HiddenField('Content', validators=[DataRequired()])
