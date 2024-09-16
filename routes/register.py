from flask import Blueprint, request, jsonify
from routes.models import User
from datetime import datetime
from functions.functions import generate_hash_password

register_blueprint = Blueprint('register', __name__)

@register_blueprint.route("/register", methods=["POST","GET"])
def register():
    if request.method == 'POST':
        try:
            username = request.json['username']
            email = request.json['email']
            password = request.json['password']
            password_hash = generate_hash_password(password)
            created_at = datetime.now()

            try:
                user = User.create_user(username, email, password_hash, created_at)
                response = {"mensaje": "Usuario registrado exitosamente"}
                return jsonify(response), 201
            except ValueError as e:
                response = {"error": str(e)}
                return jsonify(response), 500
            except Exception as e:
                response = {"error": str(e)}
                return jsonify(response), 500
        except Exception as e:
            response = {"error": str(e)}
            return jsonify(response), 500
    else:
        response = {"Mensaje":"Inserte parámetros de registro"} 
        return jsonify(response), 200