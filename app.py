from flask import Flask
from dotenv import load_dotenv
import os
from flask_cors import CORS
from messages import messages_bp
from auth import auth_bp
from flask_jwt_extended import JWTManager

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

secret_key = os.getenv('SECRET_KEY')

# Créer une application Flask
app = Flask(__name__)
app.obj_msg = "app"
CORS(app)

app.config['JWT_SECRET_KEY'] = secret_key 
jwt = JWTManager(app) 


app.register_blueprint(messages_bp, url_prefix='/messages')
app.register_blueprint(auth_bp)