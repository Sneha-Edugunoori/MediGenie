from flask import Blueprint, request
from api.deps import APIResponse, validate_json, hash_password, verify_password, generate_token, validate_email, validate_password_strength, validate_phone
from services.auth_service import AuthService
from schemas.auth_schemas import UserRegistrationSchema, UserLoginSchema

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/patient/signup', methods=['POST'])
@validate_json(['email', 'password', 'first_name', 'last_name', 'phone', 'date_of_birth'])
def patient_signup(data):
    try:
        # Validate email format
        if not validate_email(data['email']):
            return APIResponse.error("Invalid email format", 400)
        
        # Validate password strength
        is_valid, message = validate_password_strength(data['password'])
        if not is_valid:
            return APIResponse.error(message, 400)
        
        # Validate phone number
        if not validate_phone(data['phone']):
            return APIResponse.error("Invalid phone number format", 400)
        
        # Check if user already exists
        if AuthService.user_exists(data['email']):
            return APIResponse.error("User with this email already exists", 409)
        
        # Hash password
        data['password'] = hash_password(data['password'])
        data['user_type'] = 'patient'
        
        # Create user
        user = AuthService.create_user(data)
        
        # Generate token
        token = generate_token(user['id'], 'patient')
        
        return APIResponse.success({
            'user': {
                'id': user['id'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'user_type': 'patient'
            },
            'token': token
        }, "Patient registered successfully", 201)
        
    except Exception as e:
        return APIResponse.error("Registration failed", 500)

@auth_bp.route('/doctor/signup', methods=['POST'])
@validate_json(['email', 'password', 'first_name', 'last_name', 'phone', 'license_number', 'specialization'])
def doctor_signup(data):
    try:
        # Validate email format
        if not validate_email(data['email']):
            return APIResponse.error("Invalid email format", 400)
        
        # Validate password strength
        is_valid, message = validate_password_strength(data['password'])
        if not is_valid:
            return APIResponse.error(message, 400)
        
        # Check if user already exists
        if AuthService.user_exists(data['email']):
            return APIResponse.error("User with this email already exists", 409)
        
        # Check if license number already exists
        if AuthService.license_exists(data['license_number']):
            return APIResponse.error("License number already registered", 409)
        
        # Hash password
        data['password'] = hash_password(data['password'])
        data['user_type'] = 'doctor'
        data['verification_status'] = 'pending'
        
        # Create doctor
        doctor = AuthService.create_doctor(data)
        
        return APIResponse.success({
            'doctor': {
                'id': doctor['id'],
                'email': doctor['email'],
                'first_name': doctor['first_name'],
                'last_name': doctor['last_name'],
                'license_number': doctor['license_number'],
                'verification_status': 'pending'
            }
        }, "Doctor registration submitted for verification", 201)
        
    except Exception as e:
        return APIResponse.error("Registration failed", 500)

@auth_bp.route('/government/signup', methods=['POST'])
@validate_json(['email', 'password', 'first_name', 'last_name', 'department', 'employee_id'])
def government_signup(data):
    try:
        # Validate email format
        if not validate_email(data['email']):
            return APIResponse.error("Invalid email format", 400)
        
        # Validate password strength
        is_valid, message = validate_password_strength(data['password'])
        if not is_valid:
            return APIResponse.error(message, 400)
        
        # Check if user already exists
        if AuthService.user_exists(data['email']):
            return APIResponse.error("User with this email already exists", 409)
        
        # Hash password
        data['password'] = hash_password(data['password'])
        data['user_type'] = 'government'
        data['verification_status'] = 'pending'
        
        # Create government user
        gov_user = AuthService.create_government_user(data)
        
        return APIResponse.success({
            'user': {
                'id': gov_user['id'],
                'email': gov_user['email'],
                'first_name': gov_user['first_name'],
                'last_name': gov_user['last_name'],
                'department': gov_user['department'],
                'verification_status': 'pending'
            }
        }, "Government user registration submitted for verification", 201)
        
    except Exception as e:
        return APIResponse.error("Registration failed", 500)

@auth_bp.route('/login', methods=['POST'])
@validate_json(['email', 'password', 'user_type'])
def login(data):
    try:
        email = data['email']
        password = data['password']
        user_type = data['user_type']
        
        # Validate email format
        if not validate_email(email):
            return APIResponse.error("Invalid email format", 400)
        
        # Get user by email and type
        user = AuthService.get_user_by_email(email, user_type)
        
        if not user:
            return APIResponse.error("Invalid credentials", 401)
        
        # Verify password
        if not verify_password(password, user['password']):
            return APIResponse.error("Invalid credentials", 401)
        
        # Check verification status for doctors and government users
        if user_type in ['doctor', 'government'] and user.get('verification_status') != 'verified':
            return APIResponse.error("Account pending verification", 403)
        
        # Generate token
        token = generate_token(user['id'], user_type)
        
        # Update last login
        AuthService.update_last_login(user['id'])
        
        user_data = {
            'id': user['id'],
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'user_type': user_type
        }
        
        # Add type-specific data
        if user_type == 'doctor':
            user_data.update({
                'license_number': user['license_number'],
                'specialization': user['specialization'],
                'verification_status': user['verification_status']
            })
        elif user_type == 'government':
            user_data.update({
                'department': user['department'],
                'employee_id': user['employee_id'],
                'verification_status': user['verification_status']
            })
        
        return APIResponse.success({
            'user': user_data,
            'token': token
        }, "Login successful")
        
    except Exception as e:
        return APIResponse.error("Login failed", 500)

@auth_bp.route('/verify-doctor/<int:doctor_id>', methods=['POST'])
@validate_json(['verification_status', 'notes'])
def verify_doctor(data, doctor_id):
    try:
        verification_status = data['verification_status']
        notes = data.get('notes', '')
        
        if verification_status not in ['verified', 'rejected']:
            return APIResponse.error("Invalid verification status", 400)
        
        # Update doctor verification status
        AuthService.update_doctor_verification(doctor_id, verification_status, notes)
        
        return APIResponse.success({
            'doctor_id': doctor_id,
            'verification_status': verification_status
        }, f"Doctor {verification_status} successfully")
        
    except Exception as e:
        return APIResponse.error("Verification update failed", 500)

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # In a stateless JWT system, logout is handled client-side
    # You could implement a token blacklist here if needed
    return APIResponse.success(None, "Logged out successfully")

@auth_bp.route('/refresh-token', methods=['POST'])
def refresh_token():
    try:
        token = request.headers.get('Authorization')
        if not token:
            return APIResponse.error("Token is missing", 401)
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        # Decode token (this will raise an exception if expired)
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        
        # Generate new token
        new_token = generate_token(data['user_id'], data['user_type'])
        
        return APIResponse.success({
            'token': new_token
        }, "Token refreshed successfully")
        
    except jwt.ExpiredSignatureError:
        return APIResponse.error("Token has expired", 401)
    except jwt.InvalidTokenError:
        return APIResponse.error("Invalid token", 401)
    except Exception as e:
        return APIResponse.error("Token refresh failed", 500)