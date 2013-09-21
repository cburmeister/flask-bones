#!/user/bin/env python

import urlparse
from os import environ


class Travis(object):
    """Travis configurations for flask."""

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('CI', environ.get('CI'))
        app.config.setdefault('TRAVIS', environ.get('TRAVIS'))
        app.config.setdefault('LANG', environ.get('LANG'))
        app.config.setdefault('LC_ALL', environ.get('LC_ALL'))
        app.config.setdefault('TRAVIS_BRANCH', environ.get('TRAVIS_BRANCH'))
        app.config.setdefault('TRAVIS_BUILD_DIR', environ.get('TRAVIS_BUILD_DIR'))
        app.config.setdefault('TRAVIS_BUILD_ID', environ.get('TRAVIS_BUILD_ID'))
        app.config.setdefault('TRAVIS_BUILD_NUMBER', environ.get('TRAVIS_BUILD_NUMBER'))
        app.config.setdefault('TRAVIS_COMMIT', environ.get('TRAVIS_COMMIT'))
        app.config.setdefault('TRAVIS_COMMIT_RANGE', environ.get('TRAVIS_COMMIT_RANGE'))
        app.config.setdefault('TRAVIS_JOB_ID', environ.get('TRAVIS_JOB_ID'))
        app.config.setdefault('TRAVIS_JOB_NUMBER', environ.get('TRAVIS_JOB_NUMBER'))
        app.config.setdefault('TRAVIS_PULL_REQUEST', environ.get('TRAVIS_PULL_REQUEST'))
        app.config.setdefault('TRAVIS_SECURE_ENV_VARS', environ.get('TRAVIS_SECURE_ENV_VARS'))
        app.config.setdefault('TRAVIS_REPO_SLUG', environ.get('TRAVIS_REPO_SLUG'))
        app.config.setdefault('TRAVIS_PYTHON_VERSION', environ.get('TRAVIS_PYTHON_VERSION'))
