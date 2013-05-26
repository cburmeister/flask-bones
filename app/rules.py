from app import app
from werkzeug.routing import Rule

app.url_map.add(Rule('/', endpoint='index'))
