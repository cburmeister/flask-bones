from flask import request, redirect, url_for, render_template, abort, flash
from flask.ext.login import login_required
from app.extensions import cache
from app.utils import flash_errors
from app.user.models import User
from forms import EditUserForm, RegisterUserForm

from ..user import user


@user.route('/', defaults={'page': 1}, methods=['GET', 'POST'])
@user.route('/<int:page>', methods=['GET', 'POST'])
@login_required
def list(page=1):

    query = User.query

    possible_sorts = ['username', 'email']
    possible_orders = ['desc', 'asc']

    sort = request.values.get('sort', possible_sorts[0])
    order = request.values.get('order', possible_orders[0])

    if sort in possible_sorts and order in possible_orders:
        field = getattr(getattr(User, sort), order)
        query = query.order_by(field())

    users = query.paginate(page, 10)
    stats = User.stats()

    return render_template(
        'list.html',
        sorts=possible_sorts,
        users=users,
        stats=stats
    )


@user.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
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
@login_required
def delete(id):
    user = User.get_by_id(id)
    if not user:
        abort(404)
    user.delete()
    flash('User %s deleted' % user.username, 'success')
    return redirect(url_for('.list'))
