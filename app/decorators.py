from flask import abort, g
from functools import wraps
from models import User


def require_login():
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):

            if not g.user:
                abort(403)

            return function(*args, **kwargs)
        return wrapper
    return decorator

def require_permission(name):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):

            #if not name in [x.name for x in g.user.group.permissions]:
            #    abort(401)

            return function(*args, **kwargs)
        return wrapper
    return decorator
