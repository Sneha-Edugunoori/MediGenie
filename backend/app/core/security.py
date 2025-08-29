import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
import re
from typing import Optional, Tuple, Dict, Any

class SecurityManager:
    """Centralized security management"""
    
    @staticmethod
    def generate_salt() -> str:
        """Generate a random salt for password hashing"""
        return secrets.token_hex(32)
    
    @staticmethod
    def hash_password_with_salt(password: str, salt: str = None) -> Tuple[str, str]:
        """Hash password with salt"""
        if salt is None:
            salt = SecurityManager.generate_salt()
        
        # Combine password and salt
        password_salt = password + salt
        
        # Hash using SHA-256
        hashed = hashlib.sha256(password_salt.encode()).hexdigest()
        
        return hashed, salt
    
    @staticmethod
    def verify_password_with_salt(password: str, hashed_password: str, salt: str) -> bool:
        """Verify password against hash and salt"""
        test_hash, _ = SecurityManager.hash_password_with_salt(password, salt)
        return secrets.compare_digest(test_hash, hashed_password)
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Generate a cryptographically secure random token"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def validate_input_length(data: str, max_length: int = 1000) -> bool:
        """Validate input length to prevent buffer overflow"""
        return len(data) <= max_length
    
    @staticmethod
    def sanitize_input(data: str) -> str:
        """Basic input sanitization"""
        if not isinstance(data, str):
            return str(data)
        
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';']
        for char in dangerous_chars:
            data = data.replace(char, '')
        
        return data.strip()

class PasswordValidator:
    """Password validation utilities"""
    
    MIN_LENGTH = 8
    MAX_LENGTH = 128
    
    @classmethod
    def validate_strength(cls, password: str) -> Tuple[bool, str]:
        """Validate password strength"""
        if len(password) < cls.MIN_LENGTH:
            return False, f"Password must be at least {cls.MIN_LENGTH} characters long"
        
        if len(password) > cls.MAX_LENGTH:
            return False, f"Password must not exceed {cls.MAX_LENGTH} characters"
        
        # Check for uppercase letter
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        # Check for lowercase letter
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        # Check for digit
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        
        # Check for special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"
        
        # Check for common patterns
        common_patterns = ['123456', 'password', 'qwerty', 'abc123']
        if any(pattern in password.lower() for pattern in common_patterns):
            return False, "Password contains common patterns"
        
        return True, "Password is strong"

class TokenManager:
    """JWT token management"""
    
    @staticmethod
    def create_access_token(user_id: int, user_type: str, additional_claims: Dict = None) -> str:
        """Create JWT access token"""
        payload = {
            'user_id': user_id,
            'user_type': user_type,
            'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        
        if additional_claims:
            payload.update(additional_claims)
        
        return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def create_refresh_token(user_id: int, user_type: str) -> str:
        """Create JWT refresh token"""
        payload = {
            'user_id': user_id,
            'user_type': user_type,
            'exp': datetime.utcnow() + current_app.config['JWT_REFRESH_TOKEN_EXPIRES'],
            'iat': datetime.utcnow(),
            'type': 'refresh'
        }
        
        return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        """Decode and validate JWT token"""
        try:
            payload = jwt.decode(
                token, 
                current_app.config['JWT_SECRET_KEY'], 
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
    
    @staticmethod
    def extract_token_from_header(auth_header: str) -> Optional[str]:
        """Extract token from Authorization header"""
        if not auth_header:
            return None
        
        if auth_header.startswith('Bearer '):
            return auth_header[7:]
        
        return None

class InputValidator:
    """Input validation utilities"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        # Remove spaces and special characters
        clean_phone = re.sub(r'[^\d+]', '', phone)
        
        # Check if it matches common phone patterns
        patterns = [
            r'^\+?1?[0-9]{10}$',  # US format
            r'^\+?[1-9]\d{1,14}$'  # International format
        ]
        
        return any(re.match(pattern, clean_phone) for pattern in patterns)
    
    @staticmethod
    def validate_license_number(license_number: str) -> bool:
        """Validate medical license number format"""
        # Basic validation - alphanumeric, 6-20 characters
        pattern = r'^[A-Z0-9]{6,20}$'
        return bool(re.match(pattern, license_number.upper()))
    
    @staticmethod
    def validate_date_format(date_string: str) -> bool:
        """Validate date format (YYYY-MM-DD)"""
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(pattern, date_string):
            return False
        
        try:
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_time_format(time_string: str) -> bool:
        """Validate time format (HH:MM)"""
        pattern = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$'
        return bool(re.match(pattern, time_string))

class AuditLogger:
    """Security audit logging"""
    
    @staticmethod
    def log_login_attempt(user_id: Optional[int], email: str, success: bool, ip_address: str):
        """Log login attempt"""
        # This would typically log to a secure audit database
        log_entry = {
            'timestamp': datetime.utcnow(),
            'action': 'login_attempt',
            'user_id': user_id,
            'email': email,
            'success': success,
            'ip_address': ip_address,
            'user_agent': request.headers.get('User-Agent', '')
        }
        # TODO: Implement actual logging to database/file
        print(f"AUDIT LOG: {log_entry}")
    
    @staticmethod
    def log_sensitive_action(user_id: int, action: str, resource_type: str, resource_id: int = None):
        """Log sensitive actions like data access, modifications"""
        log_entry = {
            'timestamp': datetime.utcnow(),
            'action': action,
            'user_id': user_id,
            'resource_type': resource_type,
            'resource_id': resource_id,
            'ip_address': request.remote_addr
        }
        # TODO: Implement actual logging to database/file
        print(f"AUDIT LOG: {log_entry}")

class RateLimiter:
    """Simple rate limiting for login attempts"""
    
    def __init__(self):
        self.attempts = {}
    
    def is_rate_limited(self, identifier, max_attempts=5, window_minutes=15):
        """Check if identifier is rate limited"""
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=window_minutes)
        
        # Clean old attempts
        if identifier in self.attempts:
            self.attempts[identifier] = [
                attempt_time for attempt_time in self.attempts[identifier]
                if attempt_time > window_start
            ]
        
        # Check current attempts
        current_attempts = len(self.attempts.get(identifier, []))
        return current_attempts >= max_attempts
    
    def record_attempt(self, identifier):
        """Record a failed login attempt"""
        now = datetime.utcnow()
        if identifier not in self.attempts:
            self.attempts[identifier] = []
        self.attempts[identifier].append(now)

# Global rate limiter instance
rate_limiter = RateLimiter()