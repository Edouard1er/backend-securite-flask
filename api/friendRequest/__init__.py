from flask import Blueprint

friend_request_bp = Blueprint('friend_request_bp', __name__)

from . import views