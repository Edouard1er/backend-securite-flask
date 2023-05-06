import flask
from . import forum_bp
from flask import jsonify, request, abort
from config.config import db_name
from flask_jwt_extended import jwt_required
from utils.sqlReturn import *
import json


@forum_bp.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def get_forum():
    if request.method == 'GET':
        id = flask.request.values.get('id')
        tri = flask.request.values.get('tri')
        code_categorie = flask.request.values.get('code_categorie')
        andSql = ""
        if code_categorie and len(code_categorie) > 0:
            andSql = "AND f.code_categorie='{0}'".format(code_categorie)
        orderBy = "comment_max_date"
        if tri == "new_forum" :
            orderBy = "createdAt"
        elif tri == "most_reply":
            orderBy = "comment_number"
        else:
            orderBy = "comment_max_date"
        try:
            if id == None:
                sql = "SELECT f.*, cf.libelle_categorie, cf.color, u.pays, u.name, u.imageUrl, u.filiere, u.promotion, COUNT(cof.id) AS comment_number, MAX(cof.createdAt) AS comment_max_date from {0}.forum f INNER JOIN {0}.categorie_forum cf ON (f.code_categorie=cf.code_categorie) INNER JOIN {0}.utilisateur u ON (f.id_user=u.id) LEFT JOIN comment_forum cof ON (f.id=cof.id_forum AND cof.statut='1')  WHERE f.statut='1' AND cf.statut='1' {2} GROUP BY f.id ORDER BY {1} DESC".format(db_name, orderBy, andSql)
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
            userInfo = getCurrentUserInfo()
            id_user = userInfo["id"]
            titre = _json['titre']
            sql = "UPDATE {0}.forum SET contenu = '{2}', code_categorie = '{3}', titre = '{5}' where id = {1} AND id_user={4}".format(
                db_name, id_forum, contenu, code_categorie, id_user, titre)
            resp = update(sql)
            return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)

    if request.method == 'DELETE':
        try:
            id = flask.request.values.get('id')
            userInfo = getCurrentUserInfo()
            id_user = userInfo["id"]
            is_admin = userInfo["role"] == "ROLE_ADMIN"
            andSql = ""
            if not is_admin:
                andSql = " AND id_user='{0}'".format(id_user)
            if id == None:
                message = {
                    'status': 200,
                    'message': 'Please add ID',
                }
                resp = jsonify(message)
                resp.status_code = 200
                return resp
            else:
                sql = "UPDATE {0}.forum SET statut = '0' WHERE id={1} {2}".format(
                    db_name, id, andSql)
                resp = delete(sql=sql)
                return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)

# Route pour modifier les like
@forum_bp.route('/like', methods=['PUT'])
@jwt_required()
def update_like():
    userInfo = getCurrentUserInfo()
    id_user = userInfo["id"]
    
    if not request.json:
        abort(400)
    try:
        _json = request.json
        id = _json['id'] or ""
        
        sql = "SELECT list_like FROM {0}.forum WHERE id={1}".format(db_name, id)
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
        
        sql = "UPDATE {0}.forum SET list_like = '{1}' where id = '{2}'".format(
            db_name, list_like, id)
        resp = update(sql)
        return resp
    except Exception as e:
        return constant.resquestErrorResponse(e)