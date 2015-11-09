import os


class base_config(object):
    """Default configuration options."""
    SITE_NAME = 'Flask Bones'

    SERVER_NAME = os.environ['SERVER_NAME']
    SECRET_KEY = os.environ['SECRET_KEY']

    MAIL_SERVER = os.environ['MAILCATCHER_PORT_1025_TCP_ADDR']
    MAIL_PORT = os.environ['MAILCATCHER_PORT_1025_TCP_PORT']

    REDIS_HOST = os.environ['REDIS_PORT_6379_TCP_ADDR']
    REDIS_PORT = os.environ['REDIS_PORT_6379_TCP_PORT']

    BROKER_URL = 'redis://{}:{}'.format(REDIS_HOST, REDIS_PORT)
    BROKER_BACKEND = BROKER_URL

    CACHE_HOST = os.environ['MEMCACHED_PORT_11211_TCP_ADDR']
    CACHE_PORT = os.environ['MEMCACHED_PORT_11211_TCP_PORT']

    POSTGRES_HOST = os.environ['DB_PORT_5432_TCP_ADDR']
    POSTGRES_PORT = os.environ['DB_PORT_5432_TCP_PORT']
    POSTGRES_USER = os.environ.get('DB_ENV_USER', 'postgres')
    POSTGRES_PASS = os.environ.get('DB_ENV_PASS', 'postgres')
    POSTGRES_DB = 'postgres'

    SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s:%s/%s' % (
        POSTGRES_USER,
        POSTGRES_PASS,
        POSTGRES_HOST,
        POSTGRES_PORT,
        POSTGRES_DB
    )


class dev_config(base_config):
    """Development configuration options."""
    DEBUG = True
    ASSETS_DEBUG = True
    WTF_CSRF_ENABLED = False


class test_config(base_config):
    """Testing configuration options."""
    TESTING = True
    WTF_CSRF_ENABLED = False
