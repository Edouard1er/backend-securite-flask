
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

import mysql.connector

from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
secret_key = os.getenv('SECRET_KEY')

bcrypt = Bcrypt()

# Route pour créer un utilisateur


@users_bp.route('/', methods=['POST'])
def create_user():
    # Se connecter à la base de données MySQL
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    
    if not request.json:
        abort(400)
    try:
        _json = request.json
        
        # Récupérez les données de l'utilisateur à partir de la requête
        name = request.json.get('name')
        login = request.json.get('login')
        password = request.json.get('password')
        email = ""
        if "email" in _json:
            email = _json["email"]
        imageUrl = None
        if "imageUrl" in _json:
            imageUrl = _json['imageUrl'] or ""
        filiere = ""
        if "filiere" in _json:
            filiere = _json['filiere'] or ""
        promotion = ""
        if "promotion" in _json:
            promotion = _json['promotion'] or ""
        pays = ""
        if "pays" in _json:
            pays = _json['pays'] or ""
        role = ""
        if "role" in _json:
            role = _json['role'] or ""
        
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
        cursor.execute("INSERT INTO utilisateur (name, email, login, pwd, pays, filiere, promotion, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (name, email, login, hashed_password, pays, filiere, promotion, role))
        db.commit()

        # Retournez les données de l'utilisateur créé
        sql = "SELECT name, email, login,imageUrl, pays, filiere, promotion, role, createdAt from {0}.utilisateur where email = '{1}' and pwd ='{2}'".format(
            db_name, email, hashed_password)
        resp = requestSelect(sql=sql)
        return resp
    except Exception as e:
        return constant.resquestErrorResponse(e)
    


# Route pour lister tous les utilisateurs
@users_bp.route('/', methods=['GET'])
@jwt_required()
def list_users():
    id = flask.request.values.get('id')
    login = flask.request.values.get('login')
    
    if id == None and login == None:
        sql = "SELECT u.id, u.email, u.name, u.imageUrl, u.filiere, u.promotion, u.login, u.role, u.pays, u.online, createdAt from {0}.utilisateur u WHERE u.statut='1'".format(
        db_name)
    elif id == None and login != None:
        sql = "SELECT u.id, u.email, u.name, u.imageUrl, u.filiere, u.promotion, u.login, u.role, u.pays, u.online, createdAt from {0}.utilisateur u WHERE u.login='{1}'".format(
        db_name, login)
    else:
        sql = "SELECT u.id, u.email, u.name, u.imageUrl, u.filiere, u.promotion, u.login, u.role, u.pays, u.online, createdAt from {0}.utilisateur u WHERE u.id='{1}'".format(
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
    # Se connecter à la base de données MySQL
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    
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

# Route pour modifier un utilisateur
@users_bp.route('/admin', methods=['DELETE','PUT'])
@jwt_required()
def update_user():
    userInfo = getCurrentUserInfo()
    is_admin = userInfo["role"] == "ROLE_ADMIN"
    if not is_admin:
        return constant.resquestErrorResponse(msg="Vous n'avez pas les autorisations pour effectuer cette action", cd=403)
    if request.method == 'PUT':
        
        if not request.json:
            abort(400)
        try:
            _json = request.json
            setSql = ""
            id = _json['id']
            new_password = ""
            
            if "email" in _json:
                email = _json['email']
                setSql = ", email='{0}'".format(email)
                if not email or len(email) == 0:
                    return constant.resquestErrorResponse(msg="Tous les champs en * sont requis", cd=400)
            if "name" in _json:
                name = _json['name']
                setSql += ", name='{0}'".format(name)
                if not name or len(name) == 0:
                    return constant.resquestErrorResponse(msg="Tous les champs en * sont requis", cd=400)
            if "imageUrl" in _json:
                imageUrl = _json['imageUrl'] or ""
                setSql += ", imageUrl='{0}'".format(imageUrl)
            if "filiere" in _json:
                filiere = _json['filiere'] or ""
                setSql += ", filiere='{0}'".format(filiere)
            if "promotion" in _json:
                promotion = _json['promotion'] or ""
                setSql += ", promotion='{0}'".format(promotion) 
            if "login" in _json:
                login = _json['login'] or ""
                setSql += ", login='{0}'".format(login)
                if not login or len(login) == 0:
                    return constant.resquestErrorResponse(msg="Tous les champs en * sont requis", cd=400)
            if "pwd" in _json:
                new_password = _json['pwd']
                if not new_password or len(new_password) == 0:
                    return constant.resquestErrorResponse(msg="Tous les champs en * sont requis", cd=400)
            elif "password" in _json:
                new_password = _json['password']
                if not new_password or len(new_password) == 0:
                    return constant.resquestErrorResponse(msg="Tous les champs en * sont requis", cd=400)
            if "pays" in _json:
                pays = _json['pays'] or ""
                setSql += ", pays='{0}'".format(pays)
            if "role" in _json:
                role = _json['role'] or ""
                setSql += ", role='{0}'".format(role)
                if not role or len(role) == 0:
                    return constant.resquestErrorResponse(msg="Tous les champs en * sont requis", cd=400)
            
            
            if "pwd" in _json or "password" in _json:
                # Vérifier que le nouveau mot de passe respecte les exigences
                password_regex = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\w\s]).{8,}$')
                if not password_regex.match(new_password):
                    return constant.resquestErrorResponse(msg="Le nouveau mot de passe doit contenir au moins 8 caractères dont au moins 1 majuscule, 1 minuscule, 1 chiffre et 1 caractère spécial", cd=400)
                # Hacher le nouveau mot de passe
                hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                if(len(hashed_password) > 0):
                    setSql += ", pwd='{0}'".format(hashed_password)
            
            sql = "UPDATE {0}.utilisateur SET id = '{1}' {2} WHERE id = '{1}'".format(
                db_name, id, setSql )
            resp = update(sql)
            return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)
    
    if request.method == 'DELETE':
        try:
            id = flask.request.values.get('id')
            if id == None:
                message = {
                    'status': 200,
                    'message': 'Please add ID',
                }
                resp = jsonify(message)
                resp.status_code = 200
                return resp
            else:
                sql = "UPDATE {0}.utilisateur SET statut = '0' WHERE id={1}".format(
                    db_name, id)
                resp = delete(sql=sql)
                return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)