import flask
from . import friend_request_bp
from flask import jsonify, request, abort
from config.config import db_name
from flask_jwt_extended import jwt_required
from utils.sqlReturn import *