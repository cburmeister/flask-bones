from flask import request, redirect, url_for, render_template, flash, g
from flask_babel import gettext
from flask_login import login_required
from app.user.models import User
from .forms import EditUserForm

from ..user import user


@user.route('/list', methods=['GET', 'POST'])
@login_required
def list():

    from app.database import DataTable
    datatable = DataTable(
        model=User,
        columns=[User.remote_addr],
        sortable=[User.username, User.email, User.created_ts],
        searchable=[User.username, User.email],
        filterable=[User.active],
        limits=[25, 50, 100],
        request=request
    )

    if g.pjax:
        return render_template('users.html', datatable=datatable)

    return render_template('list.html', datatable=datatable)


@user.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    user = User.query.filter_by(id=id).first_or_404()
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        user.update()
        flash(
            gettext('User {username} edited'.format(username=user.username)),
            'success'
        )
    return render_template('edit.html', form=form, user=user)


@user.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    user = User.query.filter_by(id=id).first_or_404()
    user.delete()
    flash(
        gettext('User {username} deleted').format(username=user.username),
        'success'
    )
    return redirect(url_for('.list'))
