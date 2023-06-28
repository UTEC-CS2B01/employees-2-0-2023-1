from flask import (
    Blueprint,
    request,
    jsonify,
    abort,
    Response
)

import jwt
import datetime

from .models import User
from config.local import config

users_bp = Blueprint('/users', __name__)


@users_bp.route('/users', methods=['POST'])
def create_user():
    error_lists = []
    returned_code = 201
    try:
        body = request.get_json()

        if 'username' not in body:
            error_lists.append('username is required')
        else:
            username = body.get('username')

        if 'password' not in body:
            error_lists.append('password is required')
        else:
            password = body.get('password')

        if 'confirmationPassword' not in body:
            error_lists.append('confirmationPassword is required')
        else:
            confirmationPassword = body.get('confirmationPassword')

        user_db = User.query.filter(User.username == username).first()

        if user_db is not None:
            if user_db.username == username:
                error_lists.append(
                    'An account with this username already exists')
        else:
            if len(password) < 8:
                error_lists.append('Password must have at least 8 characters')

            if password != confirmationPassword:
                error_lists.append(
                    'password and confirmationPassword does not match')

        if len(error_lists) > 0:
            returned_code = 400
        else:
            user = User(username=username, password=password)
            user_created_id = user.insert()

            token = jwt.encode({
                'user_created_id': user_created_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, config['SECRET_KEY'], config['ALGORYTHM'])

    except Exception as e:
        print('e: ', e)
        returned_code = 500

    if returned_code == 400:
        return jsonify({

            'success': False,
            'errors': error_lists,
            'message': 'Error creating a new user'
        }), returned_code
    elif returned_code != 201:
        abort(returned_code)
    else:
        return jsonify({
            'success': True,
            'token': token,
            'user_created_id': user_created_id,
        }), returned_code


@users_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user():
    pass
