from . import auth_bp
from flask import jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from utils.sqlReturn import getOnlyData
from flask_bcrypt import Bcrypt
from config.config import db_name
import flask
from utils.sqlReturn import update, constant

bcrypt = Bcrypt()


@auth_bp.route('/login', methods=['POST'])
def login():
    login = request.json.get('login', None)
    password = request.json.get('password', None)
    if not login:
        return jsonify({"msg": "Nom d'utilisateur manquant"}), 400
    if not password:
        return jsonify({"msg": "Mot de passe manquant"}), 400
    sql = "SELECT u.id, u.email, u.name, u.imageUrl, u.filiere, u.promotion, u.pwd, u.role from utilisateur u LEFT JOIN message m ON (m.idRecepteur=u.id AND m.read=0) LEFT JOIN friend_request fr ON (u.id=fr.receiver AND fr.statut='SENT') WHERE login = '{0}'".format(login)
    response = getOnlyData(sql)
    if(len(response) == 0 or not bcrypt.check_password_hash(response[0]["pwd"], password)):
        return jsonify({"msg": "Nom d'utilisateur ou mot de passe incorrect"}), 401
    # Générer un jeton JWT avec l'identité de l'utilisateur
    access_token = create_access_token(identity=login)
    sql = "UPDATE {0}.utilisateur SET online='1' WHERE login = '{1}'".format(
        db_name, login)
    update(sql=sql)
    messageSql = "SELECT COUNT(m.id) AS message_not_read FROM {0}.message m WHERE m.read=0 AND m.idRecepteur={1} AND m.statut=1 GROUP BY m.idRecepteur".format(
        db_name, response[0]["id"]
    )
    messageResponse = getOnlyData(messageSql)
    
    invitaionSql = "SELECT COUNT(fr.id) AS invitations FROM {0}.friend_request fr WHERE fr.receiver={1} AND fr.statut='SENT' GROUP BY fr.receiver".format(
        db_name, response[0]["id"]
    )
    invitaionResponse = getOnlyData(invitaionSql)
    
    
    retour = {
        "utilisateur" : {
            "id" : response[0]["id"],
            "email" : response[0]["email"],
            "name" : response[0]["name"],
            "imageUrl" : response[0]["imageUrl"],
            "filiere" : response[0]["filiere"],
            "promotion" : response[0]["promotion"],
            "is_admin": 1 if response[0]["role"] == "ROLE_ADMIN" else 0,
            "login" : login,
            "message_not_read" : messageResponse[0]["message_not_read"],
            "invitations" : invitaionResponse[0]["invitations"]
        },
        "access_token" : access_token
    }   
    return jsonify(retour), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    login = get_jwt_identity()
    try:
        sql = "UPDATE {0}.utilisateur SET online='0' WHERE login = '{1}'".format(
            db_name, login)
        resp = update(sql=sql)
        return resp
    except Exception as e:
        return constant.resquestErrorResponse(e)
