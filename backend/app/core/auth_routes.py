from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import db, User, Patient, Doctor, GovernmentOfficial, UserRole
from .security import SecurityUtils, SessionManager, rate_limiter
from .exceptions import ValidationError, AuthenticationError, DatabaseError
from .database import DatabaseManager
import logging

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@auth_bp.route('/patient_signup', methods=['GET', 'POST'])
def patient_signup():
    if request.method == 'POST':
        try:
            # Get form data
            email = request.form.get('email', '').lower().strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            first_name = SecurityUtils.sanitize_input(request.form.get('first_name', ''))
            last_name = SecurityUtils.sanitize_input(request.form.get('last_name', ''))
            phone = request.form.get('phone', '')
            
            # Validation
            if not all([email, password, first_name, last_name]):
                raise ValidationError("All required fields must be filled")
            
            if password != confirm_password:
                raise ValidationError("Passwords do not match")
            
            SecurityUtils.validate_email(email)
            SecurityUtils.validate_phone(phone)
            
            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                raise ValidationError("Email already registered")
            
            # Create user
            user = User(
                email=email,
                password_hash=SecurityUtils.hash_password(password),
                role=UserRole.PATIENT,
                first_name=first_name,
                last_name=last_name,
                phone=phone
            )
            
            DatabaseManager.save_to_db(user)
            
            # Create patient profile
            patient = Patient(user_id=user.id)
            DatabaseManager.save_to_db(patient)
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.patient_login'))
            
        except ValidationError as e:
            flash(str(e), 'error')
        except Exception as e:
            logger.error(f"Patient signup error: {str(e)}")
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('patient_signup.html')

@auth_bp.route('/patient_login', methods=['GET', 'POST'])
def patient_login():
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').lower().strip()
            password = request.form.get('password', '')
            
            # Rate limiting
            if rate_limiter.is_rate_limited(request.remote_addr):
                raise AuthenticationError("Too many login attempts. Please try again later.")
            
            if not email or not password:
                raise ValidationError("Email and password are required")
            
            # Find user
            user = User.query.filter_by(email=email, role=UserRole.PATIENT).first()
            
            if not user or not SecurityUtils.verify_password(user.password_hash, password):
                rate_limiter.record_attempt(request.remote_addr)
                raise AuthenticationError("Invalid email or password")
            
            if not user.is_active:
                raise AuthenticationError("Account is deactivated")
            
            # Create session
            SessionManager.create_session(user.id, user.role.value, user.email)
            
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
            
        except (ValidationError, AuthenticationError) as e:
            flash(str(e), 'error')
        except Exception as e:
            logger.error(f"Patient login error: {str(e)}")
            flash('Login failed. Please try again.', 'error')
    
    return render_template('patient_login.html')

@auth_bp.route('/doctor_signup', methods=['GET', 'POST'])
def doctor_signup():
    if request.method == 'POST':
        try:
            # Get form data
            email = request.form.get('email', '').lower().strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            first_name = SecurityUtils.sanitize_input(request.form.get('first_name', ''))
            last_name = SecurityUtils.sanitize_input(request.form.get('last_name', ''))
            phone = request.form.get('phone', '')
            license_number = request.form.get('license_number', '')
            specialization = SecurityUtils.sanitize_input(request.form.get('specialization', ''))
            qualification = SecurityUtils.sanitize_input(request.form.get('qualification', ''))
            
            # Validation
            if not all([email, password, first_name, last_name, license_number]):
                raise ValidationError("All required fields must be filled")
            
            if password != confirm_password:
                raise ValidationError("Passwords do not match")
            
            SecurityUtils.validate_email(email)
            SecurityUtils.validate_phone(phone)
            
            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                raise ValidationError("Email already registered")
            
            # Check if license number already exists
            existing_doctor = Doctor.query.filter_by(license_number=license_number).first()
            if existing_doctor:
                raise ValidationError("License number already registered")
            
            # Create user
            user = User(
                email=email,
                password_hash=SecurityUtils.hash_password(password),
                role=UserRole.DOCTOR,
                first_name=first_name,
                last_name=last_name,
                phone=phone
            )
            
            DatabaseManager.save_to_db(user)
            
            # Create doctor profile
            doctor = Doctor(
                user_id=user.id,
                license_number=license_number,
                specialization=specialization,
                qualification=qualification
            )
            DatabaseManager.save_to_db(doctor)
            
            flash('Registration successful! Your account is pending verification.', 'success')
            return redirect(url_for('auth.doctor_login'))
            
        except ValidationError as e:
            flash(str(e), 'error')
        except Exception as e:
            logger.error(f"Doctor signup error: {str(e)}")
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('doctor_signup.html')

@auth_bp.route('/doctor_login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').lower().strip()
            password = request.form.get('password', '')
            
            # Rate limiting
            if rate_limiter.is_rate_limited(request.remote_addr):
                raise AuthenticationError("Too many login attempts. Please try again later.")
            
            if not email or not password:
                raise ValidationError("Email and password are required")
            
            # Find user
            user = User.query.filter_by(email=email, role=UserRole.DOCTOR).first()
            
            if not user or not SecurityUtils.verify_password(user.password_hash, password):
                rate_limiter.record_attempt(request.remote_addr)
                raise AuthenticationError("Invalid email or password")
            
            if not user.is_active:
                raise AuthenticationError("Account is deactivated")
            
            # Check if doctor is verified
            doctor = Doctor.query.filter_by(user_id=user.id).first()
            if not doctor.is_verified:
                flash('Your account is pending verification. Please wait for approval.', 'warning')
                return render_template('doctor_login.html')
            
            # Create session
            SessionManager.create_session(user.id, user.role.value, user.email)
            
            flash('Login successful!', 'success')
            return redirect(url_for('doctor_dashboard'))
            
        except (ValidationError, AuthenticationError) as e:
            flash(str(e), 'error')
        except Exception as e:
            logger.error(f"Doctor login error: {str(e)}")
            flash('Login failed. Please try again.', 'error')
    
    return render_template('doctor_login.html')

@auth_bp.route('/government_signup', methods=['GET', 'POST'])
def government_signup():
    if request.method == 'POST':
        try:
            # Get form data
            email = request.form.get('email', '').lower().strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            first_name = SecurityUtils.sanitize_input(request.form.get('first_name', ''))
            last_name = SecurityUtils.sanitize_input(request.form.get('last_name', ''))
            phone = request.form.get('phone', '')
            employee_id = request.form.get('employee_id', '')
            department = SecurityUtils.sanitize_input(request.form.get('department', ''))
            position = SecurityUtils.sanitize_input(request.form.get('position', ''))
            
            # Validation
            if not all([email, password, first_name, last_name, employee_id, department]):
                raise ValidationError("All required fields must be filled")
            
            if password != confirm_password:
                raise ValidationError("Passwords do not match")
            
            SecurityUtils.validate_email(email)
            SecurityUtils.validate_phone(phone)
            
            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                raise ValidationError("Email already registered")
            
            # Check if employee ID already exists
            existing_gov = GovernmentOfficial.query.filter_by(employee_id=employee_id).first()
            if existing_gov:
                raise ValidationError("Employee ID already registered")
            
            # Create user
            user = User(
                email=email,
                password_hash=SecurityUtils.hash_password(password),
                role=UserRole.GOVERNMENT,
                first_name=first_name,
                last_name=last_name,
                phone=phone
            )
            
            DatabaseManager.save_to_db(user)
            
            # Create government official profile
            gov_official = GovernmentOfficial(
                user_id=user.id,
                employee_id=employee_id,
                department=department,
                position=position,
                clearance_level='Level 1'  # Default clearance
            )
            DatabaseManager.save_to_db(gov_official)
            
            flash('Registration successful! Your account is pending verification.', 'success')
            return redirect(url_for('auth.government_login'))
            
        except ValidationError as e:
            flash(str(e), 'error')
        except Exception as e:
            logger.error(f"Government signup error: {str(e)}")
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('government_signup.html')

@auth_bp.route('/government_login', methods=['GET', 'POST'])
def government_login():
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').lower().strip()
            password = request.form.get('password', '')
            
            # Rate limiting
            if rate_limiter.is_rate_limited(request.remote_addr):
                raise AuthenticationError("Too many login attempts. Please try again later.")
            
            if not email or not password:
                raise ValidationError("Email and password are required")
            
            # Find user
            user = User.query.filter_by(email=email, role=UserRole.GOVERNMENT).first()
            
            if not user or not SecurityUtils.verify_password(user.password_hash, password):
                rate_limiter.record_attempt(request.remote_addr)
                raise AuthenticationError("Invalid email or password")
            
            if not user.is_active:
                raise AuthenticationError("Account is deactivated")
            
            # Create session
            SessionManager.create_session(user.id, user.role.value, user.email)
            
            flash('Login successful!', 'success')
            return redirect(url_for('government_dashboard'))
            
        except (ValidationError, AuthenticationError) as e:
            flash(str(e), 'error')
        except Exception as e:
            logger.error(f"Government login error: {str(e)}")
            flash('Login failed. Please try again.', 'error')
    
    return render_template('government_login.html')

@auth_bp.route('/logout')
def logout():
    SessionManager.destroy_session()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('home'))

@auth_bp.route('/doctor_verification')
def doctor_verification():
    # This would typically be an admin-only page
    doctors = Doctor.query.filter_by(is_verified=False).all()
    return render_template('doctor_verification.html', doctors=doctors)

@auth_bp.route('/verify_doctor/<int:doctor_id>')
def verify_doctor(doctor_id):
    try:
        doctor = Doctor.query.get_or_404(doctor_id)
        doctor.is_verified = True
        doctor.user.is_verified = True
        DatabaseManager.update_db()
        
        flash(f'Doctor {doctor.user.first_name} {doctor.user.last_name} has been verified.', 'success')
    except Exception as e:
        logger.error(f"Error verifying doctor: {str(e)}")
        flash('Error verifying doctor.', 'error')
    
    return redirect(url_for('auth.doctor_verification'))