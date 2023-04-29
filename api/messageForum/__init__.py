
from flask import Blueprint

message_forum_bp = Blueprint('message_forum_bp', __name__)

from . import views