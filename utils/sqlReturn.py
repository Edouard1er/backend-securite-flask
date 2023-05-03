from flask import Response, jsonify
import utils.constant as constant
from config.config import Config
import mysql.connector

from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
secret_key = os.getenv('SECRET_KEY')

# Créer une connexion à la base de données



def getOnlyData(sql) -> list:
    cnx = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
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
        data=data, code=200))
    resp.status_code = 200
    return resp


def update(sql):
    cnx = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    resp = jsonify(constant.requestRespond(
        data=[],
        m="Data update Failed!", code=400))
    resp.status_code = 400
    try:
        with cnx.cursor() as cursor:
            cursor.execute(sql)
            cnx.commit()
            resp = jsonify(constant.requestRespond(
                data=[],
                m="Data updated successfully!", code=200))
            resp.status_code = 200
    finally:
        cursor.close()
    return resp


def insert(sql, data):
    cnx = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    resp = jsonify(constant.requestRespond(
        data=[],
        m="Data insert Failed!", code=400))
    resp.status_code = 400
    try:
        with cnx.cursor() as cursor:
            cursor.execute(sql, data)
            cnx.commit()
            resp = jsonify(constant.requestRespond(
                data=[],
                m="Data inserted successfully!", code=200))
            resp.status_code = 200
    finally:
        cursor.close()

    return resp


def delete(sql):
    cnx = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    resp = jsonify(constant.requestRespond(
        data=[],
        m="Data delete Failed!", code=400))
    resp.status_code = 400
    try:
        with cnx.cursor() as cursor:
            cursor.execute(sql)
            cnx.commit()
        resp = jsonify(constant.requestRespond(
            data=[],
            m="Data deleted successfully!", code=200))
        resp.status_code = 200
    finally:
        cursor.close()
    return resp
