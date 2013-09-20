import os


class base_config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')


class dev_config(base_config):
    DEBUG = True
    WTF_CSRF_ENABLED = False


class test_config(base_config):
    TESTING = True
    WTF_CSRF_ENABLED = False
