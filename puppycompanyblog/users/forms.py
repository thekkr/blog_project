from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,ValidationError
from wtforms.validators import DataRequired,Email,EqualTo
from flask_wtf.file import FileAllowed,FileField

from flask_login import current_user
from puppycompanyblog.models import User

class LoginForm(FlaskForm):

    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):

    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message='passwords must match')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Register')

    def validated_email(self,email):
        if User.query.filter_by(email = self.email.data).first():
            raise ValidationError('Email is already registered')

    def validate_username(self,username):
        if User.query.filter_by(username = self.username.data).first():
            raise ValidationError('Username already Exists')


class UpdateForm(FlaskForm):

    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired()])
    picture = FileField('Update Profile Pic')
    submit = SubmitField('Update')

    def validate_email(self,email):
        if email.data!=current_user.email:
            if User.query.filter_by(email = email.data).first():
                raise ValidationError('Email already Exists')

    def validate_username(self,username):
        if username.data!=current_user.username:
            if User.query.filter_by(username = username.data).first():
                raise ValidationError('Username already Exists')
