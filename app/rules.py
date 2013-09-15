from app import app
from werkzeug.routing import Rule

app.url_map.add(Rule('/', endpoint='index'))
app.url_map.add(Rule('/login', endpoint='login'))
app.url_map.add(Rule('/logout', endpoint='logout'))

app.url_map.add(Rule('/users', endpoint='users'))
app.url_map.add(Rule('/user/create', endpoint='create_user'))
app.url_map.add(Rule('/user/<int:id>/edit', endpoint='edit_user'))
app.url_map.add(Rule('/user/<int:id>/delete', endpoint='delete_user'))

app.url_map.add(Rule('/permissions', endpoint='permissions'))
app.url_map.add(Rule('/permission/create', endpoint='create_permission'))
app.url_map.add(Rule('/permission/<int:id>/edit', endpoint='edit_permission'))
app.url_map.add(Rule('/permission/<int:id>/delete', endpoint='delete_permission'))
