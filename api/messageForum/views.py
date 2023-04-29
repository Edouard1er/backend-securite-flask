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
                sql = "SELECT * from {0}.message_forum".format(db_name)
            else:
                sql = "SELECT * from {0}.message_forum where id = {1}".format(
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
            titre = _json["titre"]
            contenu = _json["contenu"]
            id_frm = _json["id_frm"]
            id_user = _json['id_user']
            sql = "INSERT INTO {0}.message_forum (titre, contenu, id_frm, id_user) VALUES(%s,%s,%s,%s)".format(
                db_name)
            data = [titre, contenu, id_frm, id_user]
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
            id_message_forum = _json['id']
            contenu = _json['contenu']
            sql = "UPDATE {0}.message_forum SET contenu = '{1}' where id = {2}".format(
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
                sql = "DELETE FROM {0}.message_forum WHERE id = {1}".format(
                    db_name, id)
                resp = delete(sql=sql)
                return resp
        except Exception as e:
            print(e)
            return constant.resquestErrorResponse(e)


# POST Body
# {
#     "titre":"test 2",
#     "contenu":"2 bla bla bla",
#     "id_frm": 2,
#     "id_user":2
# }

# PUT
# {
#     "id":2,
#     "contenu":"test second "

# }
