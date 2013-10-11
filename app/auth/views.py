from flask import current_app, request, redirect, url_for, render_template, flash, abort
from flask.ext.login import login_user, login_required, logout_user
from flask.ext.mail import Message
from app.extensions import lm, mail
from app.utils import flash_errors
from app.user.models import User
from app.user.forms import RegisterUserForm
from .forms import LoginForm
from ..auth import auth
from ..tasks import send_email

from itsdangerous import URLSafeSerializer, BadSignature


@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        flash('You were logged in as %s' % form.user.username, 'success')
        return redirect(request.args.get('next') or url_for('index'))
    else:
        flash_errors(form)
    return render_template('login.html', form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You were logged out', 'success')
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

        msg = Message('User Registration', sender='admin@flask-bones.com', recipients=[user.email])
        msg.body = render_template('mail/registration.mail', user=user, token=token)

        send_email.delay(msg)

        flash('Sent verification email to %s' % (user.email), 'success')
        return redirect(url_for('index'))
    else:
        flash_errors(form)
    return render_template('register.html', form=form)


@auth.route('/verify/<token>', methods=['GET'])
def verify(token):
    s = URLSafeSerializer(current_app.secret_key)
    try:
        user_id = s.loads(token)
    except BadSignature:
        abort(404)

    user = User.get_by_id(user_id)
    if not user or user.active:
        abort(404)
    else:
        user.active = True
        user.update()

        flash('Registered user %s. Please login to continue.' % user.username, 'success')
        return redirect(url_for('auth.login'))
