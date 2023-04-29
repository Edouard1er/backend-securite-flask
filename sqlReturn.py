import os
from dotenv import load_dotenv
from flask import Response, jsonify
import mysql
import constant

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les informations de connexion à la base de données à partir des variables d'environnement
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

# Créer une connexion à la base de données
cnx = mysql.connector.connect(
    user=db_user, password=db_password, host=db_host, database=db_name)


def getOnlyData(sql) -> list:
    data = []
    try:
        with cnx.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
        # Get the column names for the table
        column_names = [description[0] for description in cursor.description]
    # Create a list of dictionaries, where each dictionary represents a row in the table
        data = [dict(zip(column_names, row)) for row in rows]
    finally:
        cursor.close()
    return data


def requestSelect(sql) -> Response:
    data = getOnlyData(sql)
    resp = jsonify(constant.requestRespond(
        m="data",
        data=data, code=200))
    resp.status_code = 200
    return resp


def update(sql):
    resp = jsonify(constant.requestRespond(
        data="Table update Failed!", code=400))
    resp.status_code = 400
    try:
        conn = cnx.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        resp = jsonify(constant.requestRespond(
            data="Table updated successfully!", code=200))
        resp.status_code = 200
    finally:
        cursor.close()
        conn.close()
    return resp


def insert(sql, data):
    resp = jsonify(constant.requestRespond(
        data="Table insert Failed!", code=400))
    resp.status_code = 400
    try:
        conn = cnx.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        resp = jsonify(constant.requestRespond(
            data="Table inserted successfully!", code=200))
        resp.status_code = 200
    finally:
        cursor.close()
        conn.close()
    return resp


def delete(sql):
    resp = jsonify(constant.requestRespond(
        data="Table delete Failed!", code=400))
    resp.status_code = 400
    try:
        conn = cnx.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        resp = jsonify(constant.requestRespond(
            data="Table deleted successfully!", code=200))
        resp.status_code = 200
    finally:
        cursor.close()
        conn.close()
    return resp
