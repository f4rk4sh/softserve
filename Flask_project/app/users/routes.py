from app.users import bp
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user
from app.users.forms import UserRegistrationForm, SetPasswordForm
from app.models import User
from app.users.email import send_registration_email
from app import db


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
            flash(f'A registration email has been sent to {user.email}')
            return redirect(url_for('main.index'))
    return render_template('users/register_user.html', title='Register user', form=form)


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
        return redirect(url_for('auth.login'))
    return render_template('users/set_password.html', form=form)
