from app.users import bp
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
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
            user = User(name=form.name.data,
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            send_registration_email(user)
            flash(f'A registration email has been sent to {user.email}')
            return redirect(url_for('users.user_list'))
    return render_template('form.html', title='Register user', form=form)


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
    return render_template('form.html', title='Set password', form=form)


@bp.route('/all')
@login_required
@admin_required
def user_list():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page, 10, False)
    next_url = url_for('users.user_list', page=users.next_num) if users.has_next else None
    prev_url = url_for('users.user_list', page=users.prev_num) if users.has_prev else None
    return render_template('users/user_list.html',
                           title='Users',
                           users=users.items,
                           next_url=next_url,
                           prev_url=prev_url)


@bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def user_edit(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    form = UserEditForm(user.email)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('users.user_list'))
    elif request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
    return render_template('form.html', title='Edit user', form=form)


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
