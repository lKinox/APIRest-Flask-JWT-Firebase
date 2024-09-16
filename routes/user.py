from flask import Blueprint, request, jsonify
from routes.models import Update, Delete, Authenticate
import jwt
from functions.functions import generate_token_jwt, token_required

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route("/user", methods=["GET"])
@token_required
def get_user_profile(payload):
    try:
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
            return jsonify(response)
        else:
            response = {"Mensaje": "Hubo un error encontrando su usuario"}
            return jsonify(response)

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_blueprint.route("/user", methods=["PUT"])
@token_required
def update_user_profile(payload):

    try:
        username = payload["username"]

        new_username = request.json["username"]
        email = request.json["email"]

        user = Update.update_user(username, new_username, email)

        if isinstance(user, dict) and 'error' in user:
            return jsonify(user), 400

        if user:
            token_jwt = generate_token_jwt(user)
            return jsonify({'Token': token_jwt, 'Nuevo Usuario': user.username, 'Nuevo Email': user.email})
        else:
            response = {"error": "Credenciales inválidas"}
            return jsonify(response)

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'})
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'})
    except Exception as e:
        return jsonify({'error': str(e)})


@user_blueprint.route("/user", methods=["DELETE"])
@token_required
def delete_user(payload):

    try:
        username = payload["username"]

        delete = Delete.delete_user(username)

        if isinstance(delete, dict) and 'error' in delete:
            return jsonify(delete)

        return jsonify({"Mensaje": "Usuario eliminado correctamente"})

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'})
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'})
    except Exception as e:
        return jsonify({'error': str(e)})