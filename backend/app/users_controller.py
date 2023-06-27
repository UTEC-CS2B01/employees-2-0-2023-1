from flask import (
    Blueprint,
    request,
    jsonify,
)

from .models import User, db

import sys

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

        user_db = User.query.filter(User.username == username).first()

        if 'password' not in body:
            error_lists.append('password is required')
        else:
            password = body.get('password')

        if 'confirmationPassword' not in body:
            error_lists.append('confirmationPassword is required')
        else:
            confirmationPassword = body.get('confirmationPassword')

        if user_db is not None:
            error_lists.append('Username already exists')

        if len(error_lists) == 0:
            new_user = User(username=username, password=password)

            db.session.add(new_user)
            db.session.commit()

    except Exception as e:
        print(sys.exc_info())
        db.session.rollback()
        returned_code = 500

    finally:
        db.session.close()

    if len(error_lists) > 0:
        returned_code = 400

    if returned_code == 201:
        return jsonify({'success': False, 'user': new_user.serialize}), returned_code
    elif returned_code == 400:
        return jsonify({'success': False, 'errors': error_lists}), returned_code
    else:
        return jsonify({'success': False, 'message': 'Internal server error'}), returned_code
