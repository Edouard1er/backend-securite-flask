from . import auth_bp
from flask import jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from utils.sqlReturn import getOnlyData
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


@auth_bp.route('/login', methods=['POST'])
def login():
    login = request.json.get('login', None)
    password = request.json.get('password', None)
    if not login:
        return jsonify({"msg": "Nom d'utilisateur manquant"}), 400
    if not password:
        return jsonify({"msg": "Mot de passe manquant"}), 400
    sql = "SELECT pwd from utilisateur WHERE login = '{0}'".format(login)
    response = getOnlyData(sql)
    if(len(response) == 0 or not bcrypt.check_password_hash(response[0]["pwd"], password)):
        return jsonify({"msg": "Nom d'utilisateur ou mot de passe incorrect"}), 401
    # Générer un jeton JWT avec l'identité de l'utilisateur
    access_token = create_access_token(identity=login)
    return jsonify(access_token=access_token), 200
