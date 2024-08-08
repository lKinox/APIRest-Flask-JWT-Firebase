from flask import Blueprint, request, jsonify, session, current_app
from models import Authenticate
import jwt
from functions.functions import generate_token_jwt
from functools import wraps

login_blueprint = Blueprint('login', __name__)

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = session.get('token_jwt')  # Obtén el token de la sesión
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'Message': 'Token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'Message': 'Invalid token'}), 403
        
        return func(*args, **kwargs)
    return decorated

@login_blueprint.route("/login", methods=["POST", "GET"])
def login_user():
    if request.method == 'POST':
        username = request.json["username"]
        password = request.json["password"]

        user = Authenticate.verify_user(username, password)
        session['logged_in'] = True

        if user:
            token_jwt = generate_token_jwt(user)
            session['token_jwt'] = token_jwt
            return jsonify({'mensaje': "El usuario fue autenticado satisfactoriamente"})
            
        else:
            response = {"error": "Credenciales inválidas"}
            return jsonify(response), 401
    else:
        response = {"Mensaje": "Inserte Usuario y Contraseña"}
        return jsonify(response), 200