#!/usr/bin/env python
# encoding: utf-8
__author__ = 'ethan'

from functools import wraps
from flask import abort
from flask_login import current_user
from model.base import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def panel_required(panel):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.has_panel(panel):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator
