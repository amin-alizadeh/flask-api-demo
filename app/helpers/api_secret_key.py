from functools import wraps
from flask import request, jsonify

from config import Config

def require_secret_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the secret key from headers
        secret_key = request.headers.get('secret')
        
        # Check if the key matches
        if not secret_key or secret_key != Config.API_KEY_SECRET:
            return jsonify({'error': 'Invalid or missing secret key'}), 401
        
        return f(*args, **kwargs)
    return decorated_function