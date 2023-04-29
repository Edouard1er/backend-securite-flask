from flask import Flask, request, jsonify, json, abort
import flask
import mysql.connector
from dotenv import load_dotenv
import os
from flask_cors import CORS
from sqlReturn import *


# Créer une application Flask
app = Flask(__name__)
app.obj_msg = "app"
CORS(app)

# Définir une route pour l'URL racine ("/")


@app.route("/api/message/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def getMessage():

    if request.method == 'GET':
        try:
            id = flask.request.values.get('id')
            if id == None:
                sql = "SELECT * FROM {0}.message".format(db_name)
            else:
                sql = "SELECT * FROM {0}.message where id ={1}".format(
                    db_name, id)
            resp = requestSelect(sql=sql)
            return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)
    if request.method == 'POST':
        if not request.json:
            abort(400)
        _json = request.json
        try:
            # Remove later //TODO
            message = {
                'status': 200,
                'message': 'Sucess',
            }
            resp = jsonify(message)
            resp.status_code = 200
            return resp
        except Exception as e:
            return constant.resquestErrorResponse(e)

# ---------------------------------------------------NO FOUND ERROR ---------------------------------------------------------------------------------------------


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
