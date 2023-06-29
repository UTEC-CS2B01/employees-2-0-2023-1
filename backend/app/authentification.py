from functools import wraps
from flask import request, jsonify
import jwt
import sys

from config.local import config

def authorize(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'X-ACCESS-TOKEN' in request.headers:
            token = request.headers['X-ACCESS-TOKEN']
        if token is None:
            return jsonify({
                'success': False,
                'message': 'Unathenticated users',
            }, 401)
        
        try:
            jwt.decode(token, config.get('SECRET_KEY'), algorithms=config.get('ALGORITHM'))
            print('\tDecoded token: ')
        except Exception as e:
            print('e', e)
            print('sys.exc_info()', sys.exc_info())
            return jsonify({
                'success': False,
                'message': 'Token is invalid, try again'
            }, 401)
        return f(*args, **kwargs)
    
    decorator.__name__ = f.__name__
    return decorator
