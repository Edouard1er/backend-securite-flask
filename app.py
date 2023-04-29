from flask import Flask, request, jsonify, json
import mysql.connector
from dotenv import load_dotenv
import os
from flask_cors import CORS

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les informations de connexion à la base de données à partir des variables d'environnement
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

# Créer une connexion à la base de données
cnx = mysql.connector.connect(user=db_user, password=db_password, host=db_host, database=db_name)

# Créer une application Flask
app = Flask(__name__)
app.obj_msg = "app"
CORS(app)


# Définir une route pour l'URL racine ("/")
@app.route("/api/message")
def index():
    # Exécuter une requête SELECT
    with cnx.cursor() as cursor:
        select_query = "SELECT * FROM message"
        cursor.execute(select_query)
        rows = cursor.fetchall()

    # Convertir le résultat en un objet JSON
    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "obj_msg": row[1],
            "contenu": row[2]
        })

    # Renvoyer la réponse JSON
    return jsonify(results)


# Définir une route pour l'opération CREATE
@app.route("/api/message", methods=["POST"])
def create():
    print(request)
    if request.method == "POST":
        # Récupérer les données du formulaire
        donnee = request.get_json()
        # print("POST")
        # Rediriger vers la page d'accueil
    return jsonify({
        "status" : "OK"
    })
    

# Définir une route pour l'opération UPDATE
@app.route("/api/message/<int:id>", methods=["GET","PUT", "DELETE"])
def message(id):
    if request.method == "GET":
        print("GET")
    elif request.method == "PUT":
        # Récupérer les données du formulaire
        donnee = request.get_json()
        print("PUT")
                
        cnx.commit()    
    elif request.method == "DELETE":
        print("DELETE")
        
    return jsonify({
        "status" : "OK"
    })
