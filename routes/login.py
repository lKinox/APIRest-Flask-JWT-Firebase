from flask import Blueprint, request, jsonify, session, current_app
from routes.models import Authenticate
from functions.functions import generate_token_jwt

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route("/login", methods=["POST", "GET"])
def login_user():
    if request.method == 'POST':
        username = request.json["username"]
        password = request.json["password"]

        user = Authenticate.verify_user(username, password)

        if user:
            token_jwt = generate_token_jwt(user)
            return jsonify({'token': token_jwt})
            
        else:
            response = {"error": "Credenciales inválidas"}
            return jsonify(response), 401
    else:
        response = {"Mensaje": "Inserte Usuario y Contraseña"}
        return jsonify(response), 200