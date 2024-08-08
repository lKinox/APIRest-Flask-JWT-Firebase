from flask import Blueprint, request, jsonify, session, current_app
from routes.login import token_required
from models import Update, Delete, Authenticate
import jwt
from functions.functions import generate_token_jwt

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route("/user", methods=["GET"])
@token_required
def get_user_profile():
    token = session.get('token_jwt')

    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        username = payload["username"]

        user_info = Authenticate.get_user(username)

        if user_info:
            username, email, id, created_at = user_info
            response = {
                "Usuario": username,
                "Email": email,
                "ID": id,
                "Created At": created_at
            }
            return jsonify(response), 200
        else:
            response = {"Mensaje": "Hubo un error encontrando su usuario"}
            return jsonify(response), 401

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_blueprint.route("/user", methods=["PUT"])
@token_required
def update_user_profile():
    token = session.get('token_jwt')

    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        username = payload["username"]

        new_username = request.json["username"]
        email = request.json["email"]

        user = Update.update_user(username, new_username, email)

        if isinstance(user, dict) and 'error' in user:
            return jsonify(user), 400

        if user:
            token_jwt = generate_token_jwt(user)
            session['token_jwt'] = token_jwt
            return jsonify({'Token': token_jwt, 'Nuevo Usuario': user.username, 'Nuevo Email': user.email})
        else:
            response = {"error": "Credenciales inválidas"}
            return jsonify(response), 401

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_blueprint.route("/user", methods=["DELETE"])
@token_required
def delete_user():
    token = session.get('token_jwt')

    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        username = payload["username"]

        delete = Delete.delete_user(username)

        if isinstance(delete, dict) and 'error' in delete:
            return jsonify(delete), 400

        if delete:
            session.clear()
            response = {"Mensaje": "Usuario eliminado correctamente"}
            return jsonify(response), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500