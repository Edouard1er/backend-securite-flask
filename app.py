from datetime import timedelta
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from flask_cors import CORS
from api.messages import messages_bp
from api.auth import auth_bp
from api.forum import forum_bp
from api.messageForum import message_forum_bp
from api.admin import admin_bp
from api.categorieForum import categorie_forum_bp
from api.temoignage import temoignage_bp
from api.friend import friend_bp
from api.friendRequest import friend_request_bp

from flask_jwt_extended import JWTManager
from api.users import users_bp

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

secret_key = os.getenv('SECRET_KEY')

# Créer une application Flask
app = Flask(__name__)
app.obj_msg = "app"
CORS(app)

app.config['JWT_SECRET_KEY'] = secret_key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

app.register_blueprint(messages_bp, url_prefix='/api/messages')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(forum_bp, url_prefix='/api/forums')
app.register_blueprint(temoignage_bp, url_prefix='/api/temoignages')
app.register_blueprint(friend_bp, url_prefix='/api/friends')
app.register_blueprint(message_forum_bp, url_prefix='/api/forum/comments')
app.register_blueprint(categorie_forum_bp, url_prefix='/api/forum/categories')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(friend_request_bp, url_prefix='/api/friend/requests')


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
        'data': [],

    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.errorhandler(500)
def not_found(error=None):
    message = {
        'status': 500,
        'message': "Votre requeste n'est pas correcte",
        'data': [],

    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
