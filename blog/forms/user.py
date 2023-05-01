from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class UserRegisterForm(FlaskForm):
    username = StringField('username')
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('E-mail', [DataRequired(), Email()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm_password', message='Field must be equal to password'),
    ])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    #csrf_token = StringField('csrf_token', validators=[DataRequired()])