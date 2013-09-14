from flask import Flask, request, g
from flask.ext.heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy
import time

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgresql://cburmeister@localhost/flask_bones'

app = Flask(__name__)
app.config.from_object(__name__)

heroku = Heroku(app)
db = SQLAlchemy(app)

from app import views
from app import models


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: '%.5fs' % (time.time() - g.request_start_time)
