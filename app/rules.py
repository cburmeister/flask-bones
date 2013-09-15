from app import app
from werkzeug.routing import Rule

app.url_map.add(Rule('/', endpoint='index'))
app.url_map.add(Rule('/login', endpoint='login'))
app.url_map.add(Rule('/logout', endpoint='logout'))
app.url_map.add(Rule('/admin', endpoint='admin'))
app.url_map.add(Rule('/create_user', endpoint='create_user'))
