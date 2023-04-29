from flask import Blueprint, jsonify, request

# Créez une instance de Blueprint pour les utilisateurs
users_bp = Blueprint('users', __name__)

from . import views