from app.main import bp
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required


@bp.route('/')
def index():
    return render_template('main/index.html')

