import flask
from . import forum_bp
from flask import jsonify, request, abort
from config.config import db_name
from flask_jwt_extended import jwt_required
from utils.sqlReturn import *


@forum_bp.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def get_forum():
    if request.method == 'GET':
        id = flask.request.values.get('id')
        try:
            if id == None:
                sql = "SELECT * from {0}.forum".format(db_name)
            else:
                sql = "SELECT * from {0}.forum where id = {1}".format(
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
            descript = _json['description']
            sql = "INSERT INTO {0}.forum (description) VALUES(%s)".format(
                db_name)
            data = [descript]
            resp = insert(sql=sql, data=data)
            return resp
        except Exception as e:
            print(e)
            return constant.resquestErrorResponse(e)

    if request.method == 'PUT':
        if not request.json:
            abort(400)
        try:
            _json = request.json
            id_forum = _json['id']
            descript = _json['description']
            sql = "UPDATE {0}.forum SET description = '{1}' where id = {2}".format(
                db_name, descript, id_forum)
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
                sql = "DELETE FROM {0}.forum WHERE id = {1}".format(
                    db_name, id)
                resp = delete(sql=sql)
                return resp
        except Exception as e:
            print(e)
            return constant.resquestErrorResponse(e)


#
# PUT  body
# {
#     "id":1,
#     "description":"here 1"
# }


# POST, DELETE  body
# {
#     "description":"here 1"
# }
