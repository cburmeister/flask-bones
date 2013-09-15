from flask import flash
from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectMultipleField, widgets
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

from models import Permission

def flash_errors(form, category='danger'):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), category)


class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class CreateUserForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    email = TextField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class EditUserForm(Form):
    username = TextField('Name', validators=[DataRequired()])
    email = TextField('Email', validators=[DataRequired()])
    permissions = QuerySelectMultipleField(
            query_factory=Permission.query.all,
            get_label=lambda a: a.desc,
            widget=widgets.ListWidget(prefix_label=False),
            option_widget=widgets.CheckboxInput()
    )
