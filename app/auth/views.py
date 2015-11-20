from flask import (
    current_app, request, redirect, url_for, render_template, flash, abort,
)
from flask.ext.babel import gettext
from flask.ext.login import login_user, login_required, logout_user
from itsdangerous import URLSafeSerializer, BadSignature
from app.extensions import lm
from app.tasks import send_registration_email
from app.user.models import User
from app.user.forms import RegisterUserForm
from .forms import LoginForm
from ..auth import auth


@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        flash(
            gettext(
                'You were logged in as {username}'.format(
                    username=form.user.username
                ),
            ),
            'success'
        )
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash(gettext('You were logged out'), 'success')
    return redirect(url_for('.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():

        user = User.create(
            username=form.data['username'],
            email=form.data['email'],
            password=form.data['password'],
            remote_addr=request.remote_addr,
        )

        s = URLSafeSerializer(current_app.secret_key)
        token = s.dumps(user.id)

        send_registration_email.delay(user, token)

        flash(
            gettext(
                'Sent verification email to {email}'.format(
                    email=user.email
                )
            ),
            'success'
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@auth.route('/verify/<token>', methods=['GET'])
def verify(token):
    s = URLSafeSerializer(current_app.secret_key)
    try:
        id = s.loads(token)
    except BadSignature:
        abort(404)

    user = User.query.filter_by(id=id).first_or_404()
    if user.active:
        abort(404)
    else:
        user.active = True
        user.update()

        flash(
            gettext(
                'Registered user {username}. Please login to continue.'.format(
                    username=user.username
                ),
            ),
            'success'
        )
        return redirect(url_for('auth.login'))
