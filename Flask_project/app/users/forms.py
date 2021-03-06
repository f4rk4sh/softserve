from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, length

from app.models import User


class UserRegistrationForm(FlaskForm):
    name = StringField("Full name", validators=[DataRequired(), length(max=100)])
    email = EmailField(
        "Email address", validators=[DataRequired(), Email(), length(max=100)]
    )
    is_admin = BooleanField("Admin")
    is_recruiter = BooleanField("Recruiter")
    submit = SubmitField("Send invitation")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class SetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Confirm")


class UserEditForm(FlaskForm):
    name = StringField("Full name", validators=[DataRequired(), length(max=100)])
    email = EmailField("Email", validators=[DataRequired(), Email(), length(max=100)])
    submit = SubmitField("Confirm")

    def __init__(self, original_email, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError("Please use a different email.")
