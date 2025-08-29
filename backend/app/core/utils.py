import os
import logging
from datetime import datetime
from flask import current_app
from werkzeug.utils import secure_filename

def setup_logging():
    """Setup application logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('healthcare_app.log'),
            logging.StreamHandler()
        ]
    )
    
    # Set specific logger levels
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file, folder_name='general'):
    """Save uploaded file securely"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Add timestamp to filename to avoid conflicts
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        
        # Create folder if it doesn't exist
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder_name)
        os.makedirs(upload_path, exist_ok=True)
        
        # Save file
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)
        
        return filename
    
    return None

def format_datetime(dt, format_str='%Y-%m-%d %H:%M'):
    """Format datetime for display"""
    if isinstance(dt, str):
        return dt
    return dt.strftime(format_str) if dt else ''

def format_date(date_obj, format_str='%Y-%m-%d'):
    """Format date for display"""
    if isinstance(date_obj, str):
        return date_obj
    return date_obj.strftime(format_str) if date_obj else ''

def calculate_age(birth_date):
    """Calculate age from birth date"""
    if not birth_date:
        return None
    
    today = datetime.utcnow().date()
    age = today.year - birth_date.year
    
    # Adjust if birthday hasn't occurred this year
    if today < birth_date.replace(year=today.year):
        age -= 1
    
    return age

def paginate_query(query, page, per_page=20):
    """Paginate a SQLAlchemy query"""
    return query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

def get_status_badge_class(status):
    """Get CSS class for status badges"""
    status_classes = {
        'scheduled': 'badge-primary',
        'confirmed': 'badge-success', 
        'completed': 'badge-info',
        'cancelled': 'badge-danger',
        'no_show': 'badge-warning'
    }
    return status_classes.get(status.lower() if isinstance(status, str) else status.value.lower(), 'badge-secondary')

def generate_unique_id(prefix=''):
    """Generate unique ID with optional prefix"""
    from uuid import uuid4
    return f"{prefix}{uuid4().hex[:8]}" if prefix else uuid4().hex[:8]

def validate_date_range(start_date, end_date):
    """Validate date range"""
    if start_date and end_date:
        if start_date > end_date:
            raise ValidationError("Start date must be before end date")
    return True

def format_phone_number(phone):
    """Format phone number for display"""
    if not phone:
        return ''
    
    # Remove all non-digit characters
    clean_phone = ''.join(filter(str.isdigit, phone))
    
    # Format based on length
    if len(clean_phone) == 10:
        return f"({clean_phone[:3]}) {clean_phone[3:6]}-{clean_phone[6:]}"
    elif len(clean_phone) == 11 and clean_phone[0] == '1':
        return f"+1 ({clean_phone[1:4]}) {clean_phone[4:7]}-{clean_phone[7:]}"
    else:
        return phone  # Return original if can't format

def create_notification(user_id, title, message):
    """Create a notification for a user"""
    from .models import Notification
    from .database import DatabaseManager
    
    try:
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message
        )
        DatabaseManager.save_to_db(notification)
        return notification
    except Exception as e:
        logging.error(f"Error creating notification: {str(e)}")
        return None

def log_user_action(user_id, action, resource_type=None, resource_id=None, details=None):
    """Log user action for audit trail"""
    from .models import AuditLog
    from .database import DatabaseManager
    from flask import request
    
    try:
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=request.remote_addr if request else None,
            user_agent=request.headers.get('User-Agent') if request else None
        )
        DatabaseManager.save_to_db(audit_log)
        return audit_log
    except Exception as e:
        logging.error(f"Error logging user action: {str(e)}")
        return None

def get_dashboard_stats(user_role, user_id=None):
    """Get dashboard statistics based on user role"""
    from .models import Patient, Doctor, Appointment, MedicalRecord
    
    stats = {}
    
    try:
        if user_role == UserRole.PATIENT:
            if user_id:
                patient = Patient.query.filter_by(user_id=user_id).first()
                if patient:
                    stats = {
                        'total_appointments': Appointment.query.filter_by(patient_id=patient.id).count(),
                        'upcoming_appointments': Appointment.query.filter(
                            Appointment.patient_id == patient.id,
                            Appointment.appointment_date > datetime.utcnow()
                        ).count(),
                        'total_records': MedicalRecord.query.filter_by(patient_id=patient.id).count()
                    }
        
        elif user_role == UserRole.DOCTOR:
            if user_id:
                doctor = Doctor.query.filter_by(user_id=user_id).first()
                if doctor:
                    stats = {
                        'total_patients': db.session.query(Patient.id).join(Appointment)
                            .filter(Appointment.doctor_id == doctor.id).distinct().count(),
                        'total_appointments': Appointment.query.filter_by(doctor_id=doctor.id).count(),
                        'completed_appointments': Appointment.query.filter_by(
                            doctor_id=doctor.id,
                            status=AppointmentStatus.COMPLETED
                        ).count()
                    }
        
        elif user_role == UserRole.GOVERNMENT:
            stats = {
                'total_patients': Patient.query.count(),
                'total_doctors': Doctor.query.count(),
                'total_appointments': Appointment.query.count(),
                'total_records': MedicalRecord.query.count()
            }
    
    except Exception as e:
        logging.error(f"Error getting dashboard stats: {str(e)}")
    
    return stats