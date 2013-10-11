from flask import Flask, g, render_template
from app.database import db
from app.extensions import lm, api, travis, mail, heroku, bcrypt, celery, assets
from flask.ext.assets import Bundle
from app import config
from app.user import user
from app.auth import auth
from os import environ
import time


def create_app(config=config.base_config):
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_assets(app)

    @app.before_request
    def before_request():
        g.request_start_time = time.time()
        g.request_time = lambda: '%.5fs' % (time.time() - g.request_start_time)

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    return app


def register_extensions(app):
    heroku.init_app(app)
    travis.init_app(app)
    db.init_app(app)
    api.init_app(app)
    lm.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    celery.config_from_object(app.config)


def register_assets(app):
    js = Bundle(
        'js/jquery.js',
        'js/bootstrap.min.js',
        filters='jsmin',
        output='gen/packed.js'
    )
    css = Bundle(
        'css/bootstrap.min.css',
        'css/style.css'
    )
    assets.init_app(app)
    assets.register('js_all', js)
    assets.register('css_all', css)


def register_blueprints(app):
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(auth)


def register_errorhandlers(app):
    for e in [401, 404, 500]:
        app.errorhandler(e)(render_error)


def render_error(e):
    return render_template('errors/%s.html' % e.code), e.code
