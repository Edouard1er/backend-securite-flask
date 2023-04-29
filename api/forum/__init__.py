
from flask import Blueprint

forum_bp = Blueprint('forum_bp', __name__)

from . import views