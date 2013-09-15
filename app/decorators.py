from flask import session, abort, flash, redirect, url_for, g
from functools import wraps
from models import User, Permission


def require_login():
    def decorator(function):
        def wrapper(*args, **kwargs):

            if not g.user:
                abort(401)

            return function(*args, **kwargs)
        return wrapper
    return decorator

def require_permission(desc):
    def decorator(function):
        def wrapper(*args, **kwargs):

            if not desc in [x.desc for x in g.user.permissions]:
                abort(401)

            return function(*args, **kwargs)
        return wrapper
    return decorator
