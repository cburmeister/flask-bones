from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.user.models import User


class UserForm(Form):
    username = TextField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = TextField('Email', validators=[Email(), DataRequired(), Length(max=128)])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class RegisterUserForm(UserForm):
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            EqualTo(
                'confirm',
                message='Passwords must match'
            ),
            Length(min=6, max=20)
        ]
    )
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    accept_tos = BooleanField('I accept the TOS', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('Username already registered')
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append('Email already registered')
            return False

        self.user = user
        return True


class EditUserForm(UserForm):
    is_admin = BooleanField('Admin')
    active = BooleanField('Activated')
