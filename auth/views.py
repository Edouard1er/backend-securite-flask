from . import auth_bp
from flask import jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Nom d'utilisateur manquant"}), 400
    if not password:
        return jsonify({"msg": "Mot de passe manquant"}), 400
    if username != 'utilisateur' or password != 'motdepasse':
        return jsonify({"msg": "Nom d'utilisateur ou mot de passe incorrect"}), 401
    # Générer un jeton JWT avec l'identité de l'utilisateur
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200
