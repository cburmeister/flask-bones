from flask import Flask, request, session, g
from flask.ext.heroku import Heroku
from flask.ext.gravatar import Gravatar
from flask.ext.sqlalchemy import SQLAlchemy
import time
import os

DEBUG = True
WTF_CSRF_ENABLED = False if DEBUG else True
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://cburmeister@localhost/flask_bones')
SECRET_KEY = '''\xad\x96\xf9;[\x95&\xda%(\xc9\xea\xb5\xe3\x13er.,m\xf0\xe0]\xbb'''

app = Flask(__name__)
app.config.from_object(__name__)

db = SQLAlchemy(app)
heroku = Heroku(app)
gravatar = Gravatar(app, size=100)

from models import User

@app.before_request
def before_request():
    g.user = None
    user_id = session.get('user_id', None)
    if user_id:
        user = User.query.filter_by(id=user_id).first() 
        if user:
            g.user = user

    g.request_start_time = time.time()
    g.request_time = lambda: '%.5fs' % (time.time() - g.request_start_time)

from app.user import user 
from app.auth import auth 

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(auth, url_prefix='/auth')
