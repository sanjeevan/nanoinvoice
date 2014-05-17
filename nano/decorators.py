"""Decorators"""

from functools import wraps
from flask.ext.login import current_user
from flask import g, url_for, flash, redirect, Markup, request
from flaskext.babel import gettext as _

def keep_login_url(func):
    """
    Adds attribute g.keep_login_url in order to pass the current
    login URL to login/signup links.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        g.keep_login_url = True
        return func(*args, **kwargs)
    return wrapper

def check_subscription(func):
    """Checks if the user signed up for a paid subscription """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated():
            subscription = current_user.subscription
            if not subscription.active and subscription.plan.name != 'Free':
                return redirect(url_for('subscription.create', plan_id=subscription.plan_id))
        return func(*args, **kwargs)
    return wrapper
