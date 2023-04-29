from . import messages_bp
from flask import jsonify
import mysql.connector
from config import Config
from flask_jwt_extended import jwt_required
from sqlReturn import *


db = Config.DB

@messages_bp.route('/')
@jwt_required()
def get_messages():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM message')
    result = cursor.fetchall()
    messages = []
    for row in result:
        message = {
            'id': row[0],
            'obj_msg': row[1],
            'contenu': row[2]
        }
        messages.append(message)
    return jsonify(messages)

@messages_bp.route('/<int:message_id>')
def get_message(message_id):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM message WHERE id = %s', (message_id,))
    result = cursor.fetchone()
    if result:
        message = {
            'id': result[0],
            'obj_msg': result[1],
            'contenu': result[2]
        }
        return jsonify(message)
    else:
        return jsonify({'message': 'message not found'})
