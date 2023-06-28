from flask import (
    Blueprint,
    request,
<<<<<<< HEAD
<<<<<<< HEAD
    jsonify,
    abort,
<<<<<<< HEAD
=======
<<<<<<< HEAD
    Response
=======
>>>>>>> e4941db (UTEC-0013 - decorator)
=======
>>>>>>> ddd02cd (UTEC-0013 - decorator)
<<<<<<< HEAD
>>>>>>> ff2be9a (UTEC-0013 - decorator)
=======
=======
    jsonify,
    abort,
>>>>>>> e171a95 (UTEC-0013 - decorator)
>>>>>>> 3944c9d (UTEC-0013 - decorator)
)

import jwt
import datetime

from .models import User
<<<<<<< HEAD
from config.local import config  
=======
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from config.local import config
=======
from config.local import config  
>>>>>>> e4941db (UTEC-0013 - decorator)
=======
>>>>>>> ddd02cd (UTEC-0013 - decorator)
<<<<<<< HEAD
>>>>>>> ff2be9a (UTEC-0013 - decorator)
=======
=======
from config.local import config  
>>>>>>> e171a95 (UTEC-0013 - decorator)
>>>>>>> 3944c9d (UTEC-0013 - decorator)

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

<<<<<<< HEAD
=======
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        user_db = User.query.filter(User.username == username).first()
=======
>>>>>>> ddd02cd (UTEC-0013 - decorator)
=======
>>>>>>> e171a95 (UTEC-0013 - decorator)

        if user_db is not None:
            #... 

        if user_db is not None :
            if user_db.username == username:
<<<<<<< HEAD
                error_lists.append(
                    'An account with this username already exists')
=======
>>>>>>> ff2be9a (UTEC-0013 - decorator)
        
        user_db = User.query.filter(User.username==username).first()

        if user_db is not None :
            if user_db.username == username:
                error_lists.append('An account with this username already exists')
<<<<<<< HEAD
=======
>>>>>>> e4941db (UTEC-0013 - decorator)
=======
                error_lists.append('An account with this username already exists')
>>>>>>> ddd02cd (UTEC-0013 - decorator)
>>>>>>> ff2be9a (UTEC-0013 - decorator)
        else:
            if len(password) < 8:
                error_lists.append('Password must have at least 8 characters')

<<<<<<< HEAD
<<<<<<< HEAD
            if password != confirmationPassword:
<<<<<<< HEAD
=======
<<<<<<< HEAD
                error_lists.append(
                    'password and confirmationPassword does not match')
=======
        
>>>>>>> ddd02cd (UTEC-0013 - decorator)


<<<<<<< HEAD
            token = jwt.encode({
                'user_created_id': user_created_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, config['SECRET_KEY'], config['ALGORYTHM'])
=======
>>>>>>> ff2be9a (UTEC-0013 - decorator)
                error_lists.append('password and confirmationPassword does not match')
=======
>>>>>>> ddd02cd (UTEC-0013 - decorator)


        if len(error_lists) > 0:
            returned_code = 400
        else:
            user = User(username=username, password=password)
            user_created_id = user.insert()

=======
=======
>>>>>>> 2264a0b (UTEC-0013 - decorator)
        
        user_db = User.query.filter(User.username==username).first()

        if user_db is not None :
            if user_db.username == username:
                error_lists.append('An account with this username already exists')
        else:
            if len(password) < 8:
                error_lists.append('Password must have at least 8 characters')

            if password != confirmationPassword:
                error_lists.append('password and confirmationPassword does not match')


        if len(error_lists) > 0:
            returned_code = 400
        else:
            user = User(username=username, password=password)
            user_created_id = user.insert()

>>>>>>> e171a95 (UTEC-0013 - decorator)
            token = jwt.encode({
                'user_created_id': user_created_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, config['SECRET_KEY'], config['ALGORYTHM'])
    except Exception as e:
<<<<<<< HEAD
<<<<<<< HEAD
        print('e: ', e)
        returned_code = 500

    
    if returned_code == 400:
        return jsonify({
            'success': False,
            'errors': error_lists,
            'message': 'Error creating a new user'
        })
    elif returned_code != 201:
        abort(returned_code)
    else:
        return jsonify({
            'success': True,
            'token': token,
            'user_created_id': user_created_id,
        })
    
<<<<<<< HEAD
=======
>>>>>>> e4941db (UTEC-0013 - decorator)
=======

    finally:
>>>>>>> ddd02cd (UTEC-0013 - decorator)
<<<<<<< HEAD
>>>>>>> ff2be9a (UTEC-0013 - decorator)
=======
=======
        print('e: ', e)
        returned_code = 500

    
    if returned_code == 400:
        return jsonify({
            'success': False,
            'errors': error_lists,
            'message': 'Error creating a new user'
        })
    elif returned_code != 201:
        abort(returned_code)
    else:
        return jsonify({
            'success': True,
            'token': token,
            'user_created_id': user_created_id,
        })
    
>>>>>>> e171a95 (UTEC-0013 - decorator)
>>>>>>> 3944c9d (UTEC-0013 - decorator)
