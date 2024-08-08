from flask import current_app
from datetime import datetime, timedelta
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

def generate_hash_password(password):
    if isinstance(password, list):
        password = str(password[0]) 
    return hashlib.sha256(password.encode('utf-8')).hexdigest()