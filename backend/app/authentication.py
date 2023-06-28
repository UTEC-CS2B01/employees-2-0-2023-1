<<<<<<< HEAD
from flask import (
    request,
    jsonify
)

import sys
import jwt
from config.local import config

from functools import wraps

def authorize(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'X-ACCESS-TOKEN' in request.headers:
            token = request.headers['X-ACCESS-TOKEN']

        if token is None:
            return jsonify({
                'success': False,
                'message': 'Unauthenticated user, please provide your credentials'
            }), 401
        
        try:
            data = jwt.decode(token, config['SECRET_KEY'], config['ALGORYTHM'])
            print('\tdecode token: ', data)
        except Exception as e:
            print('e: ', e)
            print('sys.exc_info(): ', sys.exc_info())
            return jsonify({
                'success': False,
                'message': 'Invalid Token, try a new token'
            })
        
        return f(*args, **kwargs)
    decorator.__name__ = f.__name__
    return decorator
=======
>>>>>>> ddd02cd (UTEC-0013 - decorator)
