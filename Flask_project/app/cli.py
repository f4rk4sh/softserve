import os
from app import db
from app.models import User


def register(app):
    @app.cli.command('create-admin')
    def create_admin():
        admin = User(first_name=os.environ.get('ADMIN_FIRST_NAME'),
                     last_name=os.environ.get('ADMIN_LAST_NAME'),
                     email=os.environ.get('ADMIN_EMAIL'),
                     is_admin=True)
        admin.set_password(os.environ.get('ADMIN_PASSWORD'))
        db.session.add(admin)
        db.session.commit()
