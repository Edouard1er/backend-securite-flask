import flask
from . import friend_request_bp
from flask import jsonify, request, abort
from config.config import db_name
from flask_jwt_extended import jwt_required
from utils.sqlReturn import *

@friend_request_bp.route('/sender', methods=['GET'])
@jwt_required()
def sender():
    userInfo = getCurrentUserInfo()
    id_user = userInfo["id"]
    whereSql = "sender={0}".format(id_user)
    receiver = flask.request.values.get('receiver')
        
    try:
        if receiver == None:
            sql = "SELECT * from {0}.friend_request WHERE {1}".format(db_name, whereSql)
        else:
            elseWhereSql = "receiver='{0}' AND sender={1}".format(receiver, id_user)
            sql = "SELECT * from {0}.friend_request WHERE {1}".format(
                db_name, elseWhereSql)
        resp = requestSelect(sql=sql)
        return resp
    except Exception as e:
        return constant.resquestErrorResponse(e)
    
@friend_request_bp.route('/receiver', methods=['GET'])
@jwt_required()
def receiver():
    userInfo = getCurrentUserInfo()
    id_user = userInfo["id"]
    whereSql = "receiver={0}".format(id_user)
    sender = flask.request.values.get('sender')
        
    try:
        if sender == None:
            sql = "SELECT * from {0}.friend_request WHERE {1}".format(db_name, whereSql)
        else:
            elseWhereSql = "receiver='{0}' AND sender={1}".format(id_user, sender)
            sql = "SELECT * from {0}.friend_request WHERE {1}".format(
                db_name, elseWhereSql)
        resp = requestSelect(sql=sql)
        return resp
    except Exception as e:
        return constant.resquestErrorResponse(e)
    

@friend_request_bp.route('/sent', methods=['POST'])
@jwt_required()
def friend_requests():
    userInfo = getCurrentUserInfo()
    id_user = userInfo["id"]
    
    if not request.json:
        abort(400)
    try:
        _json = request.json
        receiver = _json['receiver']
        sqlFriend = "SELECT * FROM {0}.friend WHERE ((user_1 = {1} AND user_2 ={2}) OR (user_2 = {1} AND user_1 ={2})) AND statut='1'".format(
            db_name, id_user, receiver)
        resultFriend = getOnlyData(sqlFriend)
        if(len(resultFriend) > 0):
            return constant.resquestErrorResponse(msg="Ces users sont deja amis", cd=400)
        sqlFriendRequest = "SELECT * FROM {0}.friend_request WHERE (sender = {1} AND receiver ={2}) OR (receiver = {1} AND sender ={2})".format(
            db_name, id_user, receiver)
        resultFriendRequest = getOnlyData(sqlFriendRequest)
        if(len(resultFriendRequest) > 0):
            if(resultFriendRequest[0]["statut"] == "CANCELED"):
                delete(sql="DELETE FROM {0}.friend_request WHERE id={1}".format(db_name, resultFriendRequest[0]["id"]))
            else:
                return constant.resquestErrorResponse(msg="il y a deja une demande en cours", cd=400)
        
        sql = "INSERT INTO {0}.friend_request (sender, receiver) VALUES(%s,%s)".format(
            db_name)
        data = [id_user, receiver]
        resp = insert(sql=sql, data=data)
        return resp
    except Exception as e:
        return constant.resquestErrorResponse(e)
        

@friend_request_bp.route('/canceled', methods=['PUT'])
@jwt_required()
def sent():
    userInfo = getCurrentUserInfo()
    id_user = userInfo["id"]
    if not request.json:
        abort(400)
    try:
        _json = request.json
        receiver = _json['receiver']
        sql = "UPDATE {0}.friend_request SET statut = 'CANCELED' WHERE sender={1} AND receiver={2}".format(
            db_name, id_user, receiver)
        resp = update(sql)
        return resp
    except Exception as e:
        return constant.resquestErrorResponse(e)

@friend_request_bp.route('/accepted', methods=['PUT'])
@jwt_required()
def accepted():
    userInfo = getCurrentUserInfo()
    id_user = userInfo["id"]
    if not request.json:
        abort(400)
    try:
        _json = request.json
        sender = _json['sender']
        sql = "UPDATE {0}.friend_request SET statut = 'ACCEPTED' WHERE sender={2} AND receiver={1}".format(
            db_name, id_user, sender)
        resp = update(sql)
        return resp
    except Exception as e:
        return constant.resquestErrorResponse(e)
    
@friend_request_bp.route('/refused', methods=['PUT'])
@jwt_required()
def refused():
    userInfo = getCurrentUserInfo()
    id_user = userInfo["id"]
    if not request.json:
        abort(400)
    try:
        _json = request.json
        sender = _json['sender']
        sql = "UPDATE {0}.friend_request SET statut = 'REFUSED' WHERE sender={2} AND receiver={1}".format(
            db_name, id_user, sender)
        resp = update(sql)
        return resp
    except Exception as e:
        return constant.resquestErrorResponse(e)
    
@friend_request_bp.route('/invitation', methods=['GET'])
@jwt_required()
def get_invit():
    try:
        userInfo = getCurrentUserInfo()
        id_user = userInfo["id"]
        
        sql = "SELECT COUNT(fr.id) AS invitations FROM {0}.friend_request fr WHERE fr.receiver={1} AND fr.statut='SENT' GROUP BY fr.receiver".format(
            db_name, id_user )
        resp = requestSelect(sql)
        return resp
    except Exception as e:
        return constant.resquestErrorResponse(e)