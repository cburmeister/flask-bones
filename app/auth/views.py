from flask import request, redirect, url_for, render_template, flash
from flask.ext.login import login_user, login_required, logout_user
from app import app, lm
from app.utils import flash_errors

from app.models import User
from .forms import LoginForm


@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        flash('You were logged in as %s' % form.user.username, 'success')
        return redirect(request.args.get('next') or url_for('index'))
    else:
        flash_errors(form)
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You were logged out', 'success')
    return redirect(url_for('.login'))
