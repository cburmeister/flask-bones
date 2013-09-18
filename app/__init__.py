from flask import Flask, g, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.gravatar import Gravatar
from flask.ext.heroku import Heroku
from flask.ext.restless import APIManager
from app.config import base_config
import time
import os


def create_app():

    app = Flask(__name__)
    app.config.from_object(base_config)
    heroku = Heroku(app)

    return app

app = create_app()

lm = LoginManager(app)
db = SQLAlchemy(app)
api = APIManager(app, flask_sqlalchemy_db=db)
gravatar = Gravatar(app, size=100)

from app.user import user
from app.auth import auth

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(auth)


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: '%.5fs' % (time.time() - g.request_start_time)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/tos', methods=['GET'])
def tos():
    return render_template('tos.html')


@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error(e):
    return render_template('500.html'), 500
