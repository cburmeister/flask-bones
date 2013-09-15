from flask import Flask, request, session, g
from flask.ext.heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy
import time

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgresql://cburmeister@localhost/flask_bones'
SECRET_KEY = '''\xad\x96\xf9;[\x95&\xda%(\xc9\xea\xb5\xe3\x13er.,m\xf0\xe0]\xbb'''
WTF_CSRF_ENABLED = False if DEBUG else True

app = Flask(__name__)
app.config.from_object(__name__)

heroku = Heroku(app)
db = SQLAlchemy(app)

from app import views
from models import User

@app.before_request
def before_request():
    g.user = None
    user_id = session.get('user_id', None)
    user = User.query.filter_by(id=user_id).first() 
    if user:
        g.user = user

    g.request_start_time = time.time()
    g.request_time = lambda: '%.5fs' % (time.time() - g.request_start_time)
