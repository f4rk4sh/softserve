from flask_login import current_user
from functools import wraps
from flask import flash, redirect, url_for


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            flash('You do not have permission to access this resource.')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return decorated_view


def no_authentication_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            flash('You are already logged in.')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return decorated_view
