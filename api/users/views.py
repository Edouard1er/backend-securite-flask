
from utils.constant import *
from . import users_bp
from flask import jsonify, request
from flask_bcrypt import Bcrypt
from config.config import Config, db_name
from utils.sqlReturn import *
from flask_jwt_extended import jwt_required, get_jwt_identity
import flask
from flask import jsonify, request, abort
import re


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
    cursor.execute("INSERT INTO utilisateur (name, email, login, pwd) VALUES (%s, %s, %s, %s)",
                   (name, email, login, hashed_password))
    db.commit()

    # Retournez les données de l'utilisateur créé
    sql = "SELECT * from {0}.utilisateur where email = {1} and pwd ='{2}'".format(
        db_name, email, hashed_password)
    resp = requestSelect(sql=sql)
    return resp


# Route pour lister tous les utilisateurs
@users_bp.route('/', methods=['GET'])
@jwt_required()
def list_users():
    id = flask.request.values.get('id')
    login = flask.request.values.get('login')
    
    if id == None and login == None:
        sql = "SELECT u.id, u.email, u.name, u.imageUrl, u.filiere, u.promotion, u.login from {0}.utilisateur u WHERE u.statut='1'".format(
        db_name)
    elif id == None and login != None:
        sql = "SELECT u.id, u.email, u.name, u.imageUrl, u.filiere, u.promotion, u.login from {0}.utilisateur u WHERE u.login='{1}'".format(
        db_name, login)
    else:
        sql = "SELECT u.id, u.email, u.name, u.imageUrl, u.filiere, u.promotion, u.login from {0}.utilisateur u WHERE u.id='{1}'".format(
        db_name, id)
    resp = requestSelect(sql=sql)
    return resp

# Route pour modifier son profil
@users_bp.route('/profil', methods=['PUT'])
@jwt_required()
def update_profile():
    login = get_jwt_identity()
    if not request.json:
        abort(400)
    try:
        _json = request.json
        email = _json['email']
        name = _json['name']
        imageUrl = _json['imageUrl'] or ""
        filiere = _json['filiere'] or ""
        promotion = _json['promotion'] or ""
        
        sql = "UPDATE {0}.utilisateur SET email = '{1}', name = '{2}', imageUrl = '{3}', filiere = '{4}', promotion = '{5}' where login = '{6}'".format(
            db_name, email, name, imageUrl, filiere, promotion, login)
        resp = update(sql)
        return resp
    except Exception as e:
        return constant.resquestErrorResponse(e)


# Route pour changer le mot de passe de l'utilisateur connecté
@users_bp.route('/password', methods=['PUT'])
@jwt_required()
def change_password():
    login = get_jwt_identity()
    if not request.json:
        abort(400)

    # Récupérer les données du nouveau mot de passe depuis la requête
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')
    confirm_password = request.json.get('confirm_password')

    # Vérifier que toutes les données sont présentes
    if not old_password or not new_password or not confirm_password:
        return constant.resquestErrorResponse(msg="Tous les champs sont requis", cd=400)

    # Vérifier que le nouveau mot de passe respecte les exigences
    password_regex = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\w\s]).{8,}$')
    if not password_regex.match(new_password):
        return constant.resquestErrorResponse(msg="Le nouveau mot de passe doit contenir au moins 8 caractères dont au moins 1 majuscule, 1 minuscule, 1 chiffre et 1 caractère spécial", cd=400)

    # Vérifier que le nouveau mot de passe et la confirmation sont identiques
    if new_password != confirm_password:
        return constant.resquestErrorResponse(msg="Le nouveau mot de passe et la confirmation ne sont pas identiques", cd=400)
    
    # Vérifier que le nouveau mot de passe et la confirmation sont different
    if new_password == old_password:
        return constant.resquestErrorResponse(msg="Le nouveau mot de passe et la confirmation ne sont pas differents", cd=400)

    # Vérifier que le mot de passe actuel est correct
    cursor = db.cursor()
    cursor.execute("SELECT pwd FROM utilisateur WHERE login=%s", (login,))
    user = cursor.fetchone()
    if not bcrypt.check_password_hash(user[0], old_password):
        return constant.resquestErrorResponse(msg="Le mot de passe actuel est incorrect", cd=400)

    # Hacher le nouveau mot de passe
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

    # Mettre à jour le mot de passe de l'utilisateur dans la base de données
    cursor.execute("UPDATE utilisateur SET pwd=%s WHERE login=%s", (hashed_password, login))
    db.commit()

    # Retourner une réponse de réussite
    return jsonify({'msg': 'Le mot de passe a été modifié avec succès'}), 200
