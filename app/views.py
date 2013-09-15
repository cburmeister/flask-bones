from flask import request, redirect, url_for, render_template, session, abort, flash
from app import app, rules, db
from decorators import require_permission, require_login
from forms import LoginForm, CreateUserForm, EditUserForm, flash_errors
from models import User, Permission


@app.endpoint('index')
def index():
    return render_template('index.html')

@app.endpoint('login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.data['username']).first()
        if user and user.check_password(form.data['password']):
            session['user_id'] = user.id
            flash('You were logged in', 'success')
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash('Incorrect Username/Password', 'danger')
    else:
        flash_errors(form)
    return render_template('login.html', form=form)

@app.endpoint('logout')
@require_login()
def logout():
    session.pop('user_id', None)
    flash('You were logged out', 'success')
    return redirect(url_for('login'))

@app.endpoint('users')
@require_login()
@require_permission('users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.endpoint('create_user')
@require_login()
@require_permission('create_user')
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit(): 
        user = User.query.filter_by(username=form.data['username']).first()
        if user:
            flash('Username/Email Taken', 'warning')
        else:
            user = User(**form.data)
            db.session.add(user)
            db.session.commit()
            flash('User %s created' % user.username, 'success')
            return redirect(url_for('admin'))
    else:
        flash_errors(form)
    return render_template('create_user.html', form=form)

@app.endpoint('edit_user')
@require_login()
@require_permission('edit_user')
def edit_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        abort(404)
    data = {
        "username": user.username,
        "email": user.email,
        "permissions": user.permissions
    }
    form = EditUserForm(**data)
    if form.validate_on_submit(): 
        #form.populate_obj(user)
        user.username = form.data['username']
        user.email = form.data['email']
        user.permissions = []
        db.session.commit()
        flash('User %s edited' % user.username, 'success')
        return redirect(url_for('admin'))
    else:
        flash_errors(form)
    return render_template('edit_user.html', form=form, user=user)


@app.endpoint('delete_user')
@require_login()
@require_permission('delete_user')
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    flash('User %s deleted' % user.username, 'success')
    return redirect(url_for('admin'))


@app.endpoint('permissions')
@require_login()
@require_permission('permissions')
def permissions():
    permissions = Permission.query.all()
    return render_template('permissions.html', permissions=permissions)
