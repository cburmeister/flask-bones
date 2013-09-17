from flask import request, redirect, url_for, render_template, session, flash
from app import app
from app.utils import flash_errors
from app.decorators import require_login

from .forms import LoginForm


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['user_id'] = form.user.id
        flash('You were logged in as %s' % form.user.username, 'success')
        return redirect(request.args.get('next') or url_for('index'))
    else:
        flash_errors(form)
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
@require_login()
def logout():
    session.pop('user_id', None)
    flash('You were logged out', 'success')
    return redirect(url_for('.login'))
