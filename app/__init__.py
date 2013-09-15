from flask import Flask, request, session, g
from flask.ext.heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy
from os import environ
import time

DEBUG = True
SECRET_KEY = '''\xad\x96\xf9;[\x95&\xda%(\xc9\xea\xb5\xe3\x13er.,m\xf0\xe0]\xbb'''
WTF_CSRF_ENABLED = False if DEBUG else True
SQLALCHEMY_DATABASE_URI = 'postgresql://cburmeister@localhost/flask_bones'
#SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') 

app = Flask(__name__)
app.config.from_object(__name__)

heroku = Heroku(app)
db = SQLAlchemy(app)

from app import views
from models import User, Permission

@app.before_request
def before_request():
    g.user = None
    user_id = session.get('user_id', None)
    if user_id:
        user = User.query.filter_by(id=user_id).first() 
        if user:
            g.user = user

    g.permissions = []
    if g.user:
        permissions = Permission.query.filter_by(master_id=None)
        for p in permissions:
            sub_permissions = []
            sub_permissions.append(p)
            sub_permissions.extend([x for x in Permission.query.filter_by(master_id=p.id)])
            g.permissions.append(sub_permissions)

    g.request_start_time = time.time()
    g.request_time = lambda: '%.5fs' % (time.time() - g.request_start_time)
