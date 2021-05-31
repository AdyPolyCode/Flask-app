from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User, Post
from flask_login import current_user


class RegisterForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=14)])
    
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=16)])
    
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])

    gender = RadioField('Gender', validators=[DataRequired()], choices=['Male', 'Female'])
    
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f'Email {email.data} is already taken, please choose a different.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f'Username {username.data} is already taken, please choose a different.')


class LoginForm(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=16)])
    
    remember = BooleanField('Remember me?')
    
    submit = SubmitField('Login')


class UpdateAccount(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=14)])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=16)])

    picture = FileField('New Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(f'Email {email.data} is already taken, please choose a different.')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(f'Username {username.data} is already taken, please choose a different.')


class DeleteAccount(FlaskForm):

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])

    acknowledge = BooleanField('Agree', validators=[DataRequired()])

    submit = SubmitField('Delete')


class PostForm(FlaskForm):

    title = StringField('Title', validators=[DataRequired(), Length(min=4, max=24)])

    content = TextAreaField('Content', validators=[DataRequired(), Length(min=10, max=1000)])
    
    submit = SubmitField('Add Post')

    def validate_title(self, title):
        post = Post.query.filter_by(title=title.data).first()
        if post:
            raise ValidationError('This title is already used, please choose a different.')


class EditPostForm(FlaskForm):

    title = StringField('New Title', validators=[DataRequired(), Length(min=4, max=24)])

    content = TextAreaField('New Content', validators=[DataRequired(), Length(min=10, max=1000)])

    submit = SubmitField('Update')

    def validate_title(self, title):
        post = Post.query.filter_by(title=title.data).first()
        if post:
            raise ValidationError('This title is already used, please choose a different.')