from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = TextField('Name', validators=[DataRequired()])
    password = TextField('Password', validators=[DataRequired()])

class UserForm(Form):
    username = TextField('Name', validators=[DataRequired()])
    email = TextField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
