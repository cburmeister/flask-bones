from flask.ext.login import LoginManager
lm = LoginManager()

from flask.ext.restless import APIManager
api = APIManager()

from flask.ext.travis import Travis
travis = Travis()
