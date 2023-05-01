import flask
from . import friend_bp
from flask import jsonify, request, abort
from config.config import db_name
from flask_jwt_extended import jwt_required
from utils.sqlReturn import *


@friend_bp.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def get_message_forum():
    if request.method == 'GET':
        id = flask.request.values.get('id')
        try:
            sql = "SELECT * FROM friend f WHERE (f.user_1={1} OR f.user_2={1}) AND statut='1'".format(
                db_name, id)
            resp = getOnlyData(sql=sql)
            listFriend = []
            if(resp and len(resp) > 0):
                for item in resp:
                    if str(item["user_1"]) == str(id):
                        listFriend.append(item["user_2"])
                    else:
                        listFriend.append(item["user_1"])
                idString = str(tuple(listFriend))
            else:
                idString = "('')"
            
            sql = "SELECT u.id, u.email, u.name, u.imageUrl, u.filiere, u.promotion, u.login from {0}.utilisateur u WHERE u.statut='1' AND u.id IN {1}".format(
                db_name, idString)
            resp = requestSelect(sql=sql)
            return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)
    if request.method == 'POST':
        if not request.json:
            abort(400)
        try:
            _json = request.json
            user_1 = _json["user_1"]
            user_2 = _json["user_2"]
            sql = "INSERT INTO {0}.friend (user_1, user_2) VALUES(%s,%s)".format(
                db_name)
            data = [user_1, user_2]
            resp = insert(sql=sql, data=data)
            return resp
        except Exception as e:
            print(e)
            return constant.resquestErrorResponse(e)

    if request.method == 'DELETE':
        try:
            user_1 = flask.request.values.get('user_1')
            user_2 = flask.request.values.get('user_2')
            if user_1 == None or user_2 == None:
                message = {
                    'status': 200,
                    'message': 'Please add ID',
                }
                resp = jsonify(message)
                resp.status_code = 200
                return resp
            else:
                sql = "UPDATE {0}.friend SET statut='0' WHERE (user_1 = {1} AND user_2 ={2}) OR (user_2 = {1} AND user_1 ={2})".format(
                    db_name, user_1, user_2)
                resp = delete(sql=sql)
                return resp
        except Exception as e:
            print(e)
            return constant.resquestErrorResponse(e)
