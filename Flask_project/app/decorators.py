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


def admin_or_recruiter_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin and not current_user.is_recruiter:
            flash('You do not have permission to access this resource.')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return decorated_view


def admin_or_expert_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_recruiter:
            flash('You do not have permission to access this resource.')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return decorated_view


def expert_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_admin or current_user.is_recruiter:
            flash('You do not have permission to access this resource.')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return decorated_view
