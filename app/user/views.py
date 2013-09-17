from flask import request, redirect, url_for, render_template, session, abort, flash, g
from app import app, db
from app.decorators import require_permission, require_login
from app.utils import flash_errors
from app.models import User
from forms import CreateUserForm, EditUserForm

from ..user import user

@user.route('/list', defaults={'page': 1}, methods=['GET', 'POST'])
@user.route('/list/<int:page>', methods=['GET', 'POST'])
@require_login()
def list(page=1):
    users = User.query.paginate(page, 50)
    return render_template('list.html', users=users)

@user.route('/create', methods=['GET', 'POST'])
@require_login()
#@require_permission('View Users')
def create():
    form = CreateUserForm()
    if form.validate_on_submit(): 
        user = User.create(
            username=form.data['username'],
            email=form.data['email'],
            password=form.data['password'],
            remote_addr=request.remote_addr,
        )
        flash('User %s created' % user.username, 'success')
        return redirect(url_for('.list'))
    else:
        flash_errors(form)
    return render_template('create.html', form=form)

@user.route('/edit/<int:id>', methods=['GET', 'POST'])
@require_login()
#@require_permission('Edit User')
def edit(id):
    user = User.get_by_id(id)
    if not user:
        abort(404)
    form = EditUserForm(obj=user)
    if form.validate_on_submit(): 
        form.populate_obj(user)
        user.update()
        flash('User %s edited' % user.username, 'success')
    else:
        flash_errors(form)
    return render_template('edit.html', form=form, user=user)

@user.route('/delete/<int:id>', methods=['GET'])
@require_login()
#@require_permission('delete_user')
def delete(id):

    user = User.get_by_id(id)
    if not user or user == g.user:
        abort(404)

    user.delete()

    flash('User %s deleted' % user.username, 'success')
    return redirect(url_for('.list'))
