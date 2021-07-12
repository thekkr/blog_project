from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,ValidationError
from wtforms.validators import DataRequired,Email,EqualTo
from project.models import User
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user

class RegistrationForm(FlaskForm):

    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('Useranme',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm')])
    pass_confirm = PasswordField('Confim Password',validators=[DataRequired()])
    submit = SubmitField('Register')


    def validate_email(self,email):
        if User.query.filter_by(email = self.email.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self,username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('Useranme already exists')

class LoginForm(FlaskForm):

    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')

class UpdateForm(FlaskForm):

    email = StringField('email',validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired()])
    picture = FileField('Upload Profile pic',validators=[FileAllowed('jpg','png')])
    submit = SubmitField('Update')

    def validate_email(self,email):
        if email.data!=current_user.email:
            if User.query.filter_by(email = email.data).first():
                raise ValidationError('Email already Exists')

    def validate_username(self,username):
        if username.data!=current_user.username:
            if User.query.filter_by(username=username.data).first():
                raise ValidationError('Username already exists')
