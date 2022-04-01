from flask import render_template, current_app
from app.email import send_email


def send_reset_password_email(user):
    token = user.get_set_password_token()
    send_email('Invitation to the Interviewer',
               sender=current_app.config['MAIL_USERNAME'],
               recipients=[user.email],
               text_body=render_template('email/reset_password_email.txt', user=user, token=token),
               html_body=render_template('email/reset_password_email.html', user=user, token=token))
