from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired


class BlogPostForm(FlaskForm):
    title = StringField('title',validators=[DataRequired()])
    text = TextAreaField('text',validators=[DataRequired()])
    submit = SubmitField('Sumbit')
