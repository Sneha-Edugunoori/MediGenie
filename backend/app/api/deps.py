from functools import wraps
from flask import request, jsonify, current_app
import jwt
from datetime import datetime, timedelta
import bcrypt
import re

class APIResponse:
    @staticmethod
    def success(data=None, message="Success", status_code=200):
        response = {
            "success": True,
            "message": message,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        return jsonify(response), status_code
    
    @staticmethod
    def error(message="An error occurred", status_code=400, errors=None):
        response = {
            "success": False,
            "message": message,
            "errors": errors,
            "timestamp": datetime.utcnow().isoformat()
        }
        return jsonify(response), status_code

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return APIResponse.error("Token is missing", 401)
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
            current_user_type = data['user_type']
            
        except jwt.ExpiredSignatureError:
            return APIResponse.error("Token has expired", 401)
        except jwt.InvalidTokenError:
            return APIResponse.error("Token is invalid", 401)
        
        return f(current_user_id, current_user_type, *args, **kwargs)
    
    return decorated

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated(current_user_id, current_user_type, *args, **kwargs):
            if current_user_type not in allowed_roles:
                return APIResponse.error("Insufficient permissions", 403)
            return f(current_user_id, current_user_type, *args, **kwargs)
        return decorated
    return decorator

def validate_json(required_fields=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not request.is_json:
                return APIResponse.error("Content-Type must be application/json", 400)
            
            data = request.get_json()
            if not data:
                return APIResponse.error("No JSON data provided", 400)
            
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data or not data[field]]
                if missing_fields:
                    return APIResponse.error(
                        f"Missing required fields: {', '.join(missing_fields)}", 
                        400
                    )
            
            return f(data, *args, **kwargs)
        return decorated
    return decorator

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_token(user_id, user_type, expires_in_hours=24):
    payload = {
        'user_id': user_id,
        'user_type': user_type,
        'exp': datetime.utcnow() + timedelta(hours=expires_in_hours),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password_strength(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

def validate_phone(phone):
    pattern = r'^\+?1?[0-9]{10,15}$'
    return re.match(pattern, phone) is not None