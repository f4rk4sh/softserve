from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import db
from app.auth import bp
from app.auth.email import send_reset_password_email
from app.auth.forms import LoginForm, ResetPasswordForm, ResetPasswordRequestForm
from app.decorators import no_authentication_required
from app.models import User


@bp.route("/login", methods=["GET", "POST"])
@no_authentication_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid email address or password.")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            return redirect(url_for("main.index"))
        return redirect(next_page)
    return render_template("auth/login.html", title="Sign in", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/reset_password_request", methods=["GET", "POST"])
@no_authentication_required
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_password_email(user)
        flash("Check your email for the instructions to reset your password.")
        return redirect(url_for("auth.login"))
    return render_template("form.html", title="Reset password", form=form)


@bp.route("/reset_password/<token>", methods=["GET", "POST"])
@no_authentication_required
def reset_password(token):
    user = User.verify_set_password_token(token)
    if not user:
        return redirect(url_for("main.index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Password has been successfully reset!")
        return redirect(url_for("auth.login"))
    return render_template("form.html", title="Reset password", form=form)
