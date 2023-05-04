import flask
from . import temoignage_bp
from flask import jsonify, request, abort
from config.config import db_name
from flask_jwt_extended import jwt_required
from utils.sqlReturn import *


@temoignage_bp.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def get_message_forum():
    if request.method == 'GET':
        id = flask.request.values.get('id')
        try:
            if id == None :
                sql = "SELECT t.*, u.name, u.imageUrl, u.filiere, u.promotion from {0}.temoignage t INNER JOIN {0}.utilisateur u ON (t.id_user=u.id) WHERE t.statut='1'".format(db_name)
            else:
                sql = "SELECT t.*, u.name, u.imageUrl, u.filiere, u.promotion from {0}.temoignage t INNER JOIN {0}.utilisateur u ON (t.id_user=u.id) WHERE t.id = {1}".format(
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
            text = _json["text"]
            id_frm = _json["rating"]
            id_user = _json['id_user']
            sql = "INSERT INTO {0}.temoignage (text, rating, id_user) VALUES(%s,%s,%s)".format(
                db_name)
            data = [text, id_frm, id_user]
            resp = insert(sql=sql, data=data)
            return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)

    if request.method == 'PUT':
        if not request.json:
            abort(400)
        try:
            id_user = getCurrentUserId()
            _json = request.json
            id_temoignage = _json['id']
            text = _json['text']
            rating = _json['rating']
            sql = "UPDATE {0}.temoignage SET text = '{1}', rating={3} where id = {2} AND id_user={4}".format(
                db_name, text, id_temoignage, rating, id_user)
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
                sql = "UPDATE {0}.temoignage SET statut='0' WHERE id = {1} AND id_user={2}".format(
                    db_name, id, id_user)
                resp = delete(sql=sql)
                return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)
