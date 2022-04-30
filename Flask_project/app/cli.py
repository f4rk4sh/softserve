import click

from app import db
from app.models import User


def register(app):
    @app.cli.command("create-admin")
    @click.argument("name", metavar="<name>", required=True)
    @click.argument("email", metavar="<name>", required=True)
    @click.argument("password", metavar="<password>", required=True)
    def create_admin(name, email, password):

        """This script automatically creates admin user."""

        admin = User(name=name, email=email, is_admin=True, is_recruiter=False)

        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
