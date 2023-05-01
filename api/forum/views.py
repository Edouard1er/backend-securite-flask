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
                sql = "SELECT f.*, cf.libelle_categorie, cf.color, u.pays, u.name, u.imageUrl, u.filiere, u.promotion from {0}.forum f INNER JOIN {0}.categorie_forum cf ON (f.code_categorie=cf.code_categorie) INNER JOIN {0}.utilisateur u ON (f.id_user=u.id)  WHERE f.statut='1' AND cf.statut='1'".format(db_name)
            else:
                sql = "SELECT f.*, cf.libelle_categorie, cf.color, u.pays, u.name, u.imageUrl, u.filiere, u.promotion from {0}.forum f INNER JOIN {0}.categorie_forum cf ON (f.code_categorie=cf.code_categorie) INNER JOIN {0}.utilisateur u ON (f.id_user=u.id)  WHERE f.id = {1}".format(
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
            contenu = _json['contenu']
            code_categorie = _json['code_categorie']
            id_user = _json['id_user']
            titre = _json['titre']
            sql = "INSERT INTO {0}.forum (id_user, titre, code_categorie, contenu) VALUES(%s,%s,%s,%s)".format(
                db_name)
            data = [id_user, titre, code_categorie, contenu]
            resp = insert(sql=sql, data=data)
            return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)

    if request.method == 'PUT':
        if not request.json:
            abort(400)
        try:
            _json = request.json
            id_forum = _json['id']
            contenu = _json['contenu']
            code_categorie = _json['code_categorie']
            id_user = _json['id_user']
            titre = _json['titre']
            sql = "UPDATE {0}.forum SET contenu = '{2}', code_categorie = '{3}', id_user = '{4}', titre = '{5}' where id = {1}".format(
                db_name, id_forum, contenu, code_categorie, id_user, titre)
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
                sql = "UPDATE {0}.forum SET statut = '0' WHERE id = {1}".format(
                    db_name, id)
                resp = delete(sql=sql)
                return resp
        except Exception as e:
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
