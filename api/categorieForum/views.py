import flask
from . import categorie_forum_bp
from flask import jsonify, request, abort
from config.config import Config, db_name
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.sqlReturn import *


@categorie_forum_bp.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def get_messages():
    if request.method == 'GET':
        code_categorie = flask.request.values.get('code_categorie')
        try:
            if code_categorie == None:
                sql = "SELECT * from {0}.categorie_forum WHERE statut='1'".format(db_name)
            else:
                sql = "SELECT * from {0}.categorie_forum where code_categorie = '{1}'".format(
                    db_name, code_categorie)
            resp = requestSelect(sql=sql)
            return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)
    if request.method == 'POST':
        if not request.json:
            abort(400)
        try:
            _json = request.json
            code_categorie = _json['code_categorie']
            libelle_categorie = _json['libelle_categorie']
            sql = "INSERT INTO {0}.categorie_forum (code_categorie, libelle_categorie) VALUES(%s,%s)".format(
                db_name)
            data = [code_categorie, libelle_categorie]
            resp = insert(sql=sql, data=data)
            return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)

    if request.method == 'PUT':
        if not request.json:
            abort(400)
        try:
            _json = request.json
            id_message = _json['code_categorie']
            libelle_categorie = _json['libelle_categorie']
            sql = "UPDATE {0}.categorie_forum SET libelle_categorie = '{1}' where code_categorie = '{2}'".format(
                db_name, libelle_categorie, id_message)
            resp = update(sql)
            return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)

    if request.method == 'DELETE':
        try:
            code_categorie = flask.request.values.get('code_categorie')
            if code_categorie == None:
                categorie_forum = {
                    'status': 200,
                    'categorie_forum': 'Please add ID',
                }
                resp = jsonify(categorie_forum)
                resp.status_code = 200
                return resp
            else:
                sql = "UPDATE {0}.categorie_forum SET statut='0' WHERE code_categorie = '{1}'".format(
                    db_name, code_categorie)
                resp = delete(sql=sql)
                return resp
        except Exception as e:
            print(e)
            return constant.resquestErrorResponse(e)

# POST
# {
#     "code_categorie":"categorie_forum 2",
#     "libelle_categorie":"test 2 "
# }

# PUT
# {
#     "code_categorie":2,
#     "libelle_categorie":"test second"

# }
