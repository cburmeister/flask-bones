from flask import Flask, g, render_template
from app.database import db
from app.extensions import lm
from app.config import base_config
from app.user import user
from app.auth import auth


def create_app(config=base_config):
    app = Flask(__name__)
    app.config.from_object(config)

    from flask.ext.heroku import Heroku
    heroku = Heroku(app)

    db.init_app(app)
    lm.init_app(app)

    register_blueprints(app)
    register_errorhandlers(app)


    @app.before_request
    def before_request():
        import time
        g.request_start_time = time.time()
        g.request_time = lambda: '%.5fs' % (time.time() - g.request_start_time)

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    return app


def register_blueprints(app):
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(auth)


def register_errorhandlers(app):
    for e in [401, 404, 500]:
        app.errorhandler(e)(handle_error)


def handle_error(e):
    return render_template('errors/%s.html' % e.code), e.code
