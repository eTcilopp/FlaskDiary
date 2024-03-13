from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class BlogPostForm(FlaskForm):
    content = HiddenField('Content', validators=[DataRequired()])