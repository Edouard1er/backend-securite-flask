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
            obj_msg = _json['obj_msg']
            contenu = _json['contenu']
            sql = "INSERT INTO {0}.message (obj_msg, contenu) VALUES(%s,%s)".format(
                db_name)
            data = [obj_msg, contenu]
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
            contenu = _json['contenu']
            sql = "UPDATE {0}.message SET contenu = '{1}' where id = {2}".format(
                db_name, contenu, id_message)
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
                sql = "DELETE FROM {0}.message WHERE id = {1}".format(
                    db_name, id)
                resp = delete(sql=sql)
                return resp
        except Exception as e:
            print(e)
            return constant.resquestErrorResponse(e)

# POST
# {
#     "obj_msg":"message 2",
#     "contenu":"test 2 "
# }

# PUT
# {
#     "id":2,
#     "contenu":"test second"

# }
