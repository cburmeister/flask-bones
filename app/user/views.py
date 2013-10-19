from flask import request, redirect, url_for, render_template, flash, g
from flask.ext.login import login_required
from app.user.models import User
from forms import EditUserForm

from ..user import user


@user.route('/list', methods=['GET', 'POST'])
@login_required
def list():
    orders = ['asc', 'desc']
    limits = [25, 50, 100]

    query = User.query

    # is_sorting
    sort = request.values.get('sort', User.sortables)
    order = request.values.get('order', orders[0])
    if sort in User.sortables() and order in orders:
        query = User.sort_query(query, sort, order)

    # is_filtering
    filter = request.values.get('active', None)
    if filter:
        query = User.filter_query(query, 'active')

    # is_searching
    search = request.values.get('query', None)
    if search:
        query = User.search_query(query, search)

    users = query.paginate(
        request.values.get('page', 1, type=int),
        request.values.get('limit', limits[1], type=int)
    )
    stats = User.stats()

    if g.pjax:
        return render_template(
            'users.html',
            sorts=User.sortables(),
            limits=limits,
            users=users,
            stats=stats
        )

    return render_template(
        'list.html',
        sorts=User.sortables(),
        limits=limits,
        users=users,
        stats=stats
    )


@user.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    user = User.query.filter_by(id=id).first_or_404()
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        user.update()
        flash('User %s edited' % user.username, 'success')
    return render_template('edit.html', form=form, user=user)


@user.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    user = User.query.filter_by(id=id).first_or_404()
    user.delete()
    flash('User %s deleted' % user.username, 'success')
    return redirect(url_for('.list'))
