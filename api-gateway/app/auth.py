import functools

from flask import (
    Blueprint, g, request, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app as app
import jwt
import datetime
from app.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=["POST"])
def register():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()
            
            auth_token = encode_auth_token(user['id'])
            response = {'auth_token': auth_token}
            return jsonify(response), 201

        return {'error': error}, 400

    return {'error': 'Method not allowed'}, 405


@bp.route('/login', methods=["POST"])
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            auth_token = encode_auth_token(user['id'])
            response = {'auth_token': auth_token}
            return jsonify(response), 200

        return {'error': error}, 400

    return {'error': 'Method not allowed'}, 405


@bp.before_app_request
def load_logged_in_user():
    g.user = None
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        resp = decode_auth_token(auth_token)
        if not isinstance(resp, str):
            g.user = get_db().execute(
                'SELECT * FROM user WHERE id = ?', (resp,)
            ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return {'info': 'Logged out'}, 200


@bp.route('/validate')
def validate_token():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        resp = decode_auth_token(auth_token)
        if not isinstance(resp, str):
            return {'message': 'Token is valid.'}, 200
        return {'message': resp}, 401
    return {'message': 'Provide a valid auth token.'}, 401


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return {'error': 'Provide a valid auth token.'}, 401
        return view(**kwargs)
    return wrapped_view


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), algorithms=["HS256"])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

