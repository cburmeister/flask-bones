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

from app.user import user 
from app.auth import auth 

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(auth)

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

from flask import render_template

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/tos', methods=['GET'])
def tos():
    return render_template('tos.html')

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
