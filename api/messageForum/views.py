import flask
from . import message_forum_bp
from flask import jsonify, request, abort
from config.config import db_name
from flask_jwt_extended import jwt_required
from utils.sqlReturn import *


@message_forum_bp.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def get_message_forum():
    if request.method == 'GET':
        id = flask.request.values.get('id')
        id_forum = flask.request.values.get('id_forum')
        try:
            if id == None and id_forum == None:
                sql = "SELECT cf.*, u.name, u.imageUrl, u.filiere, u.promotion from {0}.comment_forum cf INNER JOIN {0}.utilisateur u ON (cf.id_user=u.id) WHERE cf.statut='1'".format(db_name)
            elif id == None and id_forum != None:
                sql = "SELECT cf.*, u.name, u.imageUrl, u.filiere, u.promotion from {0}.comment_forum cf INNER JOIN {0}.utilisateur u ON (cf.id_user=u.id) WHERE cf.statut='1' AND cf.id_forum={1}".format(db_name, id_forum)
            else:
                sql = "SELECT cf.*, u.name, u.imageUrl, u.filiere, u.promotion from {0}.comment_forum cf INNER JOIN {0}.utilisateur u ON (cf.id_user=u.id) WHERE cf.id = {1}".format(
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
            if id == None:
                message = {
                    'status': 200,
                    'message': 'Please add ID',
                }
                resp = jsonify(message)
                resp.status_code = 200
                return resp
            else:
                sql = "UPDATE {0}.comment_forum SET statut='0' WHERE id = {1}".format(
                    db_name, id)
                resp = delete(sql=sql)
                return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)
