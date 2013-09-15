from flask import request, redirect, url_for, render_template, session, abort, flash
from app import app, rules, db
from decorators import require_permission, require_login
from forms import LoginForm, UserForm
from models import User


@app.endpoint('index')
def index():
    return render_template('index.html')

@app.endpoint('login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(**form.data).first()
        if user:
            session['user_id'] = user.id
            flash('You were logged in')
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash('Incorrect Username/Password')
    return render_template('login.html', form=form)

@app.endpoint('logout')
@require_login()
def logout():
    session.pop('user_id', None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.endpoint('admin')
@require_login()
@require_permission('admin')
def admin():
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.endpoint('create_user')
@require_login()
@require_permission('create_user')
def create_user():
    form = UserForm()
    if form.validate_on_submit(): 
        user = User.query.filter_by(username=form.data['username']).first()
        if user:
            flash('Username/Email Taken')
        else:
            user = User(**form.data)
            db.session.add(user)
            db.session.commit()
            flash('User %s created' % user.username)
            return redirect('/admin')
    return render_template('create_user.html', form=form)
