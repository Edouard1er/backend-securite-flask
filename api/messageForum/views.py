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
        try:
            if id == None:
                sql = "SELECT * from {0}.message".format(db_name)
            else:
                sql = "SELECT * from {0}.message where id = {1}".format(
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
            # TODO
            # sql = "INSERT INTO {0}.cours ( id_enseignant, id_ue) VALUES(%s,%s)".format(
            #     dataName)
            # data = (id_enseignant, id_ue)
            # resp = insert(sql=sql, data=data)
            # TODO REMOVE later
            message = {
                'status': 200,
                'message': 'sucess',
            }
            resp = jsonify(message)
            resp.status_code = 200
            return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)

    if request.method == 'PUT':
        if not request.json:
            abort(400)
        try:
            _json = request.json
            # TODO
            # id_cours = _json['id_cours']
            # id_enseignant = _json['id_enseignant']
            # id_ue = _json['id_ue']
            # sql = "UPDATE {0}.cours SET id_enseignant = '{1}', id_ue = '{2}' where id_cours= {3}".format(
            #     dataName, id_enseignant, id_ue, id_cours)
            # resp = update(sql)
            # TODO REMOVE later
            message = {
                'status': 200,
                'message': 'sucess',
            }
            resp = jsonify(message)
            resp.status_code = 200
            return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)

    if request.method == 'DELETE':
        try:
            # sql = "DELETE FROM {0}.cours WHERE id_cours = {1}".format(
            #     dataName, id)
            # resp = requestSelect(sql=sql)
            # TODO REMOVE later
            message = {
                'status': 200,
                'message': 'sucess',
            }
            resp = jsonify(message)
            resp.status_code = 200
            return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)
