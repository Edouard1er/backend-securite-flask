import flask
from . import message_forum_bp
from flask import jsonify, request, abort
from config.config import db_name
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.sqlReturn import *
import json


@message_forum_bp.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def get_message_forum():
    if request.method == 'GET':
        id = flask.request.values.get('id')
        id_forum = flask.request.values.get('id_forum')
        tri = flask.request.values.get('tri') or "DESC"
        try:
            if id == None and id_forum == None:
                sql = "SELECT cf.*, u.name, u.imageUrl, u.filiere, u.promotion,u .pays from {0}.comment_forum cf INNER JOIN {0}.utilisateur u ON (cf.id_user=u.id) WHERE cf.statut='1' ORDER BY cf.createdAt {1}".format(db_name, tri)
            elif id == None and id_forum != None:
                sql = "SELECT cf.*, u.name, u.imageUrl, u.filiere, u.promotion,u .pays from {0}.comment_forum cf INNER JOIN {0}.utilisateur u ON (cf.id_user=u.id) WHERE cf.statut='1' AND cf.id_forum={1}  ORDER BY cf.createdAt {2}".format(db_name, id_forum, tri)
            else:
                sql = "SELECT cf.*, u.name, u.imageUrl, u.filiere, u.promotion,u .pays from {0}.comment_forum cf INNER JOIN {0}.utilisateur u ON (cf.id_user=u.id) WHERE cf.id = {1}".format(
                    db_name, id)
            resp = requestSelect(sql=sql)
            return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)
    if request.method == 'POST':
        if not request.json:
            abort(400)
        try:
            _json = request.json
            contenu = _json["contenu"]
            id_frm = _json["id_forum"]
            id_user = _json['id_user']
            sql = "INSERT INTO {0}.comment_forum (contenu, id_forum, id_user) VALUES(%s,%s,%s)".format(
                db_name)
            data = [contenu, id_frm, id_user]
            resp = insert(sql=sql, data=data)
            return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)

    if request.method == 'PUT':
        if not request.json:
            abort(400)
        try:
            _json = request.json
            id_message_forum = _json['id']
            contenu = _json['contenu']
            sql = "UPDATE {0}.comment_forum SET contenu = '{1}' where id = {2}".format(
                db_name, contenu, id_message_forum)
            resp = update(sql)
            return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)

    if request.method == 'DELETE':
        try:
            id = flask.request.values.get('id')
            id_user = getCurrentUserId()
            if id == None:
                message = {
                    'status': 200,
                    'message': 'Please add ID',
                }
                resp = jsonify(message)
                resp.status_code = 200
                return resp
            else:
                sql = "UPDATE {0}.comment_forum SET statut='0' WHERE id = {1} AND id_user={2}".format(
                    db_name, id, id_user)
                resp = delete(sql=sql)
                return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)

# Route pour modifier les like
@message_forum_bp.route('/like', methods=['PUT'])
@jwt_required()
def update_profile():
    id_user = getCurrentUserId()
    
    if not request.json:
        abort(400)
    try:
        _json = request.json
        id = _json['id'] or ""
        
        sql = "SELECT list_like FROM {0}.comment_forum WHERE id={1}".format(db_name, id)
        list_like_str = getOnlyData(sql)
        list_like = []
        if len(list_like_str) == 1:
            list_like_str = list_like_str[0]["list_like"]
        else:
            list_like_str = ""
        if list_like_str and len(list_like_str) > 0:
            list_like = json.loads(list_like_str)
            if id_user in list_like:
                list_like.remove(id_user)
            else:
                list_like.append(id_user)
            list_like_str = json.dumps(list_like)
        
        sql = "UPDATE {0}.comment_forum SET list_like = '{1}' where id = '{2}'".format(
            db_name, list_like, id)
        resp = update(sql)
        return resp
    except Exception as e:
        return constant.resquestErrorResponse(e)