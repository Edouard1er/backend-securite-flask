import flask
from . import messages_bp
from flask import jsonify, request, abort
from config.config import Config, db_name
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.sqlReturn import *


@messages_bp.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def get_messages():
    if request.method == 'GET':
        userInfo = getCurrentUserInfo()
        idEmeteur  = flask.request.values.get('idEmeteur') or userInfo["id"]
        idRecepteur = flask.request.values.get('idRecepteur')
        try:
            sql = "SELECT m.idEmeteur AS OWNER, m.content, m.time, m.read FROM {0}.message m WHERE ((m.idEmeteur={1} AND m.idRecepteur={2}) OR (m.idRecepteur={1} AND m.idEmeteur={2})) AND m.statut ='1' ORDER BY m.time".format(db_name, idEmeteur, idRecepteur)
            resp = requestSelect(sql=sql)
            return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)
    if request.method == 'POST':
        if not request.json:
            abort(400)
        try:
            _json = request.json
            idEmeteur = _json['idEmeteur']
            idRecepteur = _json['idRecepteur']
            content = _json['content']
            sql = "INSERT INTO {0}.message (idEmeteur, idRecepteur, content) VALUES(%s,%s,%s)".format(
                db_name)
            data = [idEmeteur, idRecepteur, content]
            resp = insert(sql=sql, data=data)
            return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)

    if request.method == 'PUT':
        if not request.json:
            abort(400)
        try:
            _json = request.json
            id_message = _json['id']
            content = _json['content']
            userInfo = getCurrentUserInfo()
            idEmeteur = userInfo["id"]
            sql = "UPDATE {0}.message SET content = '{1}' where id = {2} AND idEmeteur={3}".format(
                db_name, content, id_message,idEmeteur)
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
                userInfo = getCurrentUserInfo()
                idEmeteur = userInfo["id"]
                sql = "UPDATE {0}.message SET statut='0' WHERE id = {1} AND idEmeteur={2}".format(
                    db_name, id, idEmeteur)
                resp = delete(sql=sql)
                return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)

@messages_bp.route('/read', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def update_messages_read():
    if not request.json:
        abort(400)
    try:
        _json = request.json
        userInfo = getCurrentUserInfo()
        idEmeteur = _json['idEmeteur'] or userInfo["id"]
        idRecepteur = _json['idRecepteur']
        sql = "UPDATE {0}.message m SET m.read='1' where idEmeteur={1} AND idRecepteur={2}".format(
            db_name, idEmeteur, idRecepteur )
        resp = update(sql)
        return resp
    except Exception as e:
        return constant.resquestErrorResponse(e)
    
@messages_bp.route('/discussion', methods=['GET'])
@jwt_required()
def get_discussion_list():
    try:
        userInfo = getCurrentUserInfo()
        id_user = userInfo["id"]
        
        sql = "SELECT u.online, u.email, u.name, u.imageUrl, u.filiere, u.promotion, u.login, u.pays, u.role, IF(m.idEmeteur = {1}, m.idRecepteur, m.idEmeteur) AS id_user, MAX(m.time) AS last_message_time, SUM(CASE WHEN m.read = 0 AND m.idRecepteur={1} THEN 1 ELSE 0 END) as unread_count FROM  {0}.message m JOIN {0}.utilisateur u ON u.id = IF(m.idEmeteur = {1}, m.idRecepteur, m.idEmeteur) WHERE  m.idEmeteur = {1} OR m.idRecepteur = {1} GROUP BY  IF(m.idEmeteur = {1}, m.idRecepteur, m.idEmeteur) ORDER BY  last_message_time DESC".format(
            db_name, id_user )
        resp = requestSelect(sql)
        return resp
    except Exception as e:
        return constant.resquestErrorResponse(e)