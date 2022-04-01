from app.auth import bp
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from app.auth.forms import LoginForm, UserRegistrationForm, SetPasswordForm
from app.models import User
from werkzeug.urls import url_parse
from app.auth.email import send_registration_email
from app import db


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('main.index'))
        return redirect(url_for(next_page))
    return render_template('auth/login.html', title='Sign in', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
    form = UserRegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            send_registration_email(user)
            flash(f'A registration email has been sent to {user.email}.')
            return redirect(url_for('main.index'))
    return render_template('auth/register_user.html', title='Register user', form=form)


@bp.route('/register/<token>', methods=['GET', 'POST'])
def set_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_set_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = SetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Registration has been successfully completed!')
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('auth/set_password.html', form=form)
