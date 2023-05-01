
from flask import Blueprint

friend_bp = Blueprint('friend_bp', __name__)

from . import views