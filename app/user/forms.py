from flask_wtf import Form
from flask.ext.babel import gettext
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.user.models import User


class UserForm(Form):
    username = TextField(
        gettext('Username'), validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = TextField(
        gettext('Email'), validators=[Email(), DataRequired(), Length(max=128)]
    )

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class RegisterUserForm(UserForm):
    password = PasswordField(
        gettext('Password'),
        validators=[
            DataRequired(),
            EqualTo(
                'confirm',
                message=gettext('Passwords must match')
            ),
            Length(min=6, max=20)
        ]
    )
    confirm = PasswordField(
        gettext('Confirm Password'), validators=[DataRequired()]
    )
    accept_tos = BooleanField(
        gettext('I accept the TOS'), validators=[DataRequired()]
    )

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append(gettext('Username already registered'))
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append(gettext('Email already registered'))
            return False

        self.user = user
        return True


class EditUserForm(UserForm):
    is_admin = BooleanField(gettext('Admin'))
    active = BooleanField(gettext('Activated'))
