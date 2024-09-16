from flask import current_app, request, jsonify
from datetime import datetime, timedelta
from routes.models import Authenticate
from functools import wraps
import hashlib
import jwt

def generate_token_jwt(user):
    payload = {
        "id": user.id,
        "username": user.username,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm='HS256')

    return token

def decode_token(token):
    """Decodifica un token JWT y verifica su validez."""
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Token has expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'

def generate_hash_password(password):
    if isinstance(password, list):
        password = str(password[0]) 
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def token_required(f):
    @wraps(f)
    def decorated():
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            payload = decode_token(token)
            
            

            return f(payload), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 401

    return decorated