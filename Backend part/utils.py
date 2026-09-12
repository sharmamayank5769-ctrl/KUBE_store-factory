import jwt
import datetime
import bcrypt
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "kubestorefactory-secret-key-2026"


def generate_token(username):
    token = jwt.encode(
        {
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        SECRET_KEY,
        algorithm='HS256'
    )
    return token


def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def hash_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"status": "failed", "message": "Token missing"}), 401

        try:
            token = token.split(" ")[1]
        except IndexError:
            return jsonify({"status": "failed", "message": "Invalid token format"}), 401

        decoded = verify_token(token)
        if not decoded:
            return jsonify({"status": "failed", "message": "Token invalid or expired"}), 401

        return f(*args, **kwargs)

    return decorated