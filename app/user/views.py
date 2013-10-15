from flask import request, redirect, url_for, render_template, flash, g
from flask.ext.login import login_required
from app.user.models import User
from forms import EditUserForm

from ..user import user


@user.route('/list', methods=['GET', 'POST'])
@login_required
def list():
    sorts = ['username', 'email']
    orders = ['asc', 'desc']
    limits = [25, 50, 100]

    page = request.values.get('page', 1, type=int)
    sort = request.values.get('sort', sorts[0])
    order = request.values.get('order', orders[0])
    limit = request.values.get('limit', limits[1], type=int)
    filter = request.values.get('active', None)
    search = request.values.get('query', None)

    query = User.query

    if sort in sorts and order in orders:
        field = getattr(getattr(User, sort), order)
        query = query.order_by(field())

    if filter:
        field = getattr(User, 'active')
        query = query.filter(field==filter)

    if search:
        search_query = '%%%s%%' % search
        from sqlalchemy import or_
        query = query.filter(or_(
            User.email.like(search_query),
            User.username.like(search_query)
        ))

    users = query.paginate(page, limit)
    stats = User.stats()

    if g.pjax:
        return render_template(
            'users.html',
            limits=limits,
            sorts=sorts,
            users=users,
            stats=stats
        )

    return render_template(
        'list.html',
        limits=limits,
        sorts=sorts,
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
