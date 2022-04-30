from flask import current_app, render_template

from app.email import send_email


def send_registration_email(user):
    token = user.get_set_password_token()
    send_email(
        "Invitation to the Interviewer",
        sender=current_app.config["MAIL_USERNAME"],
        recipients=[user.email],
        text_body=render_template("email/register_email.txt", user=user, token=token),
        html_body=render_template("email/register_email.html", user=user, token=token),
    )
