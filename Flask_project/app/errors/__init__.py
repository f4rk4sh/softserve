from flask import Blueprint

bp = Blueprint('erorrs', __name__)

from app.errors import handlers
