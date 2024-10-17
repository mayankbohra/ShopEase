from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, length, NumberRange


class signUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), length(min=2, max=20)])
    password1 = PasswordField('Enter your Password', validators=[DataRequired(), length(min=6)])
    password2 = PasswordField('Confirm your Password', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('Sign Up')


class loginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class passwordChangeForm(FlaskForm):
    current_password = PasswordField('Enter your Password', validators=[DataRequired(), length(min=6)])
    new_password = PasswordField('Confirm your Password', validators=[DataRequired(), length(min=6)])
    confirm_new_password = PasswordField('Confirm your Password', validators=[DataRequired(), length(min=6)])
    change_password = SubmitField('Change Password')
