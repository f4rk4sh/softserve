from app.users import bp
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app.users.forms import UserRegistrationForm, SetPasswordForm, UserEditForm
from app.models import User
from app.users.email import send_registration_email
from app import db
from app.decorators import admin_required, no_authentication_required


@bp.route('/register_user', methods=['GET', 'POST'])
@login_required
@admin_required
def register_user():
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
            return redirect(url_for('users.user_list'))
    return render_template('users/register_user.html', title='Register user', form=form)


@bp.route('/register/<token>', methods=['GET', 'POST'])
@no_authentication_required
def set_password(token):
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


@bp.route('/all')
@login_required
@admin_required
def user_list():
    users = User.query.all()
    return render_template('users/user_list.html', users=users)


@bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def user_edit(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    form = UserEditForm(user.email)
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('users.user_list'))
    elif request.method == 'GET':
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.email.data = user.email
    return render_template('users/user_edit.html', form=form)


@bp.route('/<int:user_id>/delete', methods=['GET', 'POST'])
@login_required
@admin_required
def user_delete(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    db.session.delete(user)
    if User.query.filter_by(is_admin=True).count() == 0:
        flash('You can not delete last admin user.')
        return redirect(url_for('users.user_list'))
    db.session.commit()
    flash('User has been successfully deleted.')
    return redirect(url_for('users.user_list'))
