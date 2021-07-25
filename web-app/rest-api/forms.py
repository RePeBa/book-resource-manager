from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class BookForm(FlaskForm):
    author = StringField('Author', validators=[DataRequired(), Length(min=2, max=40)])
    ocr_text = TextAreaField('Text extracted from cover of book')
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=60)])
    submit = SubmitField('Save')

class NameForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=40)])
    submit = SubmitField('Enter the site')

