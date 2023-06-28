from flask import (
    Blueprint,
    request,
)

import jwt
import datetime

from .models import User

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


        if user_db is not None:
            #... 

        if user_db is not None :
            if user_db.username == username:
                error_lists.append('An account with this username already exists')
        else:
            if len(password) < 8:
                error_lists.append('Password must have at least 8 characters')

        



    except Exception as e:

    finally:
