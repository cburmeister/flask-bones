import os


class base_config(object):
    SITE_NAME = 'Flask Bones'
    SERVER_NAME = os.environ.get('SERVER_NAME')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    BROKER_URL = os.environ.get('REDISCLOUD_URL', 'redis://127.0.0.1:6379')
    BROKER_BACKEND = os.environ.get('REDISCLOUD_URL', 'redis://127.0.0.1:6379')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = os.environ.get('MAIL_PORT', 1025)


class dev_config(base_config):
    DEBUG = True
    ASSETS_DEBUG = True
    WTF_CSRF_ENABLED = False


class test_config(base_config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    if os.environ.get('CI'):
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/flask_bones'
        SECRET_KEY = 'travis_ci_secret'
