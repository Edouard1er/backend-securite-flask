
from utils.constant import *
from . import users_bp
from flask import jsonify, request
from flask_bcrypt import Bcrypt
from config.config import Config, db_name
from utils.sqlReturn import *


bcrypt = Bcrypt()

# Se connecter à la base de données MySQL
db = Config.DB

# Route pour créer un utilisateur


@users_bp.route('/', methods=['POST'])
def create_user():
    # Récupérez les données de l'utilisateur à partir de la requête
    name = request.json.get('name')
    email = request.json.get('email')
    login = request.json.get('login')
    password = request.json.get('password')

    # Vérifiez que toutes les données sont présentes
    if not name or not email or not login or not password:
        return resquestErrorResponse(msg="Tous les champs sont requis", cd=400)
    # jsonify({'error': 'Tous les champs sont requis'}), 400

    # Vérifiez si l'utilisateur existe déjà dans la base de données
    cursor = db.cursor()
    cursor.execute("SELECT * FROM utilisateur WHERE login=%s", (login,))
    user = cursor.fetchone()
    if user:
        return resquestErrorResponse(msg="Cet utilisateur existe déjà", cd=400)
    # jsonify({'error': ''}), 400

    # Hachez le mot de passe de l'utilisateur
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Ajoutez l'utilisateur à la base de données
    cursor.execute("INSERT INTO utilisateur (nom, email, login, pwd) VALUES (%s, %s, %s, %s)",
                   (name, email, login, hashed_password))
    db.commit()

    # Retournez les données de l'utilisateur créé
    sql = "SELECT * from {0}.utilisateur where email = {1} and pwd ='{2}'".format(
        db_name, email, hashed_password)
    resp = requestSelect(sql=sql)
    return resp


# Route pour lister tous les utilisateurs
@users_bp.route('/', methods=['GET'])
def list_users():
    # Récupérez tous les utilisateurs de la base de données
    # cursor = db.cursor()
    # cursor.execute("SELECT nom, email, login FROM utilisateur")
    # utilisateur = cursor.fetchall()

    # # Retournez les données des utilisateurs sous forme de JSON
    # return jsonify(utilisateur)
    sql = "SELECT nom, email, login from {0}.utilisateur".format(
        db_name)
    resp = requestSelect(sql=sql)
    return resp
