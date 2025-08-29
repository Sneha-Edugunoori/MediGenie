from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from .models import db, User, Patient, Doctor, Appointment, MedicalRecord, HealthMetric, AppointmentStatus
from .permissions import login_required, role_required, UserRole
from .security import SecurityUtils
from .exceptions import ValidationError, ResourceNotFoundError
from .database import DatabaseManager
from datetime import datetime, timedelta
import logging

patient_bp = Blueprint('patient', __name__)
logger = logging.getLogger(__name__)

@patient_bp.route('/dashboard')
@login_required
@role_required(UserRole.PATIENT)
def dashboard():
    try:
        user_id = session.get('user_id')
        patient = Patient.query.filter_by(user_id=user_id).first()
        
        if not patient:
            flash('Patient profile not found.', 'error')
            return redirect(url_for('auth.logout'))
        
        # Get recent appointments
        recent_appointments = Appointment.query.filter_by(patient_id=patient.id)\
            .order_by(Appointment.appointment_date.desc()).limit(5).all()
        
        # Get recent health metrics
        recent_metrics = HealthMetric.query.filter_by(patient_id=patient.id)\
            .order_by(HealthMetric.recorded_at.desc()).limit(10).all()
        
        # Get upcoming appointments
        upcoming_appointments = Appointment.query.filter(
            Appointment.patient_id == patient.id,
            Appointment.appointment_date > datetime.utcnow(),
            Appointment.status.in_([AppointmentStatus.SCHEDULED, AppointmentStatus.CONFIRMED])
        ).order_by(Appointment.appointment_date.asc()).limit(3).all()
        
        dashboard_data = {
            'patient': patient,
            'recent_appointments': recent_appointments,
            'upcoming_appointments': upcoming_appointments,
            'recent_metrics': recent_metrics,
            'total_appointments': Appointment.query.filter_by(patient_id=patient.id).count(),
            'total_records': MedicalRecord.query.filter_by(patient_id=patient.id).count()
        }
        
        return render_template('dashboard.html', data=dashboard_data)
        
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        flash('Error loading dashboard.', 'error')
        return render_template('dashboard.html', data={})

@patient_bp.route('/appointments')
@login_required
@role_required(UserRole.PATIENT)
def appointments():
    try:
        user_id = session.get('user_id')
        patient = Patient.query.filter_by(user_id=user_id).first()
        
        # Get all appointments
        appointments_list = Appointment.query.filter_by(patient_id=patient.id)\
            .order_by(Appointment.appointment_date.desc()).all()
        
        # Get available doctors for booking
        doctors = Doctor.query.filter_by(is_verified=True)\
            .join(User).filter(User.is_active == True).all()
        
        return render_template('appointments.html', 
                             appointments=appointments_list, 
                             doctors=doctors)
        
    except Exception as e:
        logger.error(f"Appointments error: {str(e)}")
        flash('Error loading appointments.', 'error')
        return render_template('appointments.html', appointments=[], doctors=[])

@patient_bp.route('/book_appointment', methods=['POST'])
@login_required
@role_required(UserRole.PATIENT)
def book_appointment():
    try:
        user_id = session.get('user_id')
        patient = Patient.query.filter_by(user_id=user_id).first()
        
        doctor_id = request.form.get('doctor_id')
        appointment_date = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')
        reason = SecurityUtils.sanitize_input(request.form.get('reason', ''))
        
        if not all([doctor_id, appointment_date, appointment_time]):
            raise ValidationError("All fields are required")
        
        # Combine date and time
        appointment_datetime = datetime.strptime(f"{appointment_date} {appointment_time}", "%Y-%m-%d %H:%M")
        
        # Check if appointment is in the future
        if appointment_datetime <= datetime.utcnow():
            raise ValidationError("Appointment must be scheduled for a future time")
        
        # Check if doctor is available (simple check - no overlapping appointments)
        existing_appointment = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == appointment_datetime,
            Appointment.status.in_([AppointmentStatus.SCHEDULED, AppointmentStatus.CONFIRMED])
        ).first()
        
        if existing_appointment:
            raise ValidationError("Doctor is not available at this time")
        
        # Create appointment
        appointment = Appointment(
            patient_id=patient.id,
            doctor_id=doctor_id,
            appointment_date=appointment_datetime,
            reason=reason,
            status=AppointmentStatus.SCHEDULED
        )
        
        DatabaseManager.save_to_db(appointment)
        
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('patient.appointments'))
        
    except ValidationError as e:
        flash(str(e), 'error')
    except Exception as e:
        logger.error(f"Book appointment error: {str(e)}")
        flash('Error booking appointment.', 'error')
    
    return redirect(url_for('patient.appointments'))

@patient_bp.route('/medical-records')
@login_required
@role_required(UserRole.PATIENT)
def records():
    try:
        user_id = session.get('user_id')
        patient = Patient.query.filter_by(user_id=user_id).first()
        
        # Get all medical records
        medical_records = MedicalRecord.query.filter_by(patient_id=patient.id)\
            .order_by(MedicalRecord.record_date.desc()).all()
        
        return render_template('records.html', records=medical_records)
        
    except Exception as e:
        logger.error(f"Medical records error: {str(e)}")
        flash('Error loading medical records.', 'error')
        return render_template('records.html', records=[])

@patient_bp.route('/health-tracking')
@login_required
@role_required(UserRole.PATIENT)
def health_tracking():
    try:
        user_id = session.get('user_id')
        patient = Patient.query.filter_by(user_id=user_id).first()
        
        # Get health metrics grouped by type
        metrics = HealthMetric.query.filter_by(patient_id=patient.id)\
            .order_by(HealthMetric.recorded_at.desc()).all()
        
        # Group metrics by type for charting
        metrics_by_type = {}
        for metric in metrics:
            if metric.metric_type not in metrics_by_type:
                metrics_by_type[metric.metric_type] = []
            metrics_by_type[metric.metric_type].append(metric)
        
        return render_template('health.html', metrics=metrics, metrics_by_type=metrics_by_type)
        
    except Exception as e:
        logger.error(f"Health tracking error: {str(e)}")
        flash('Error loading health tracking data.', 'error')
        return render_template('health.html', metrics=[], metrics_by_type={})

@patient_bp.route('/add_health_metric', methods=['POST'])
@login_required
@role_required(UserRole.PATIENT)
def add_health_metric():
    try:
        user_id = session.get('user_id')
        patient = Patient.query.filter_by(user_id=user_id).first()
        
        metric_type = request.form.get('metric_type')
        value = request.form.get('value')
        unit = request.form.get('unit')
        notes = SecurityUtils.sanitize_input(request.form.get('notes', ''))
        
        if not all([metric_type, value]):
            raise ValidationError("Metric type and value are required")
        
        # Create health metric
        metric = HealthMetric(
            patient_id=patient.id,
            metric_type=metric_type,
            value=value,
            unit=unit,
            notes=notes
        )
        
        DatabaseManager.save_to_db(metric)
        
        flash('Health metric added successfully!', 'success')
        
    except ValidationError as e:
        flash(str(e), 'error')
    except Exception as e:
        logger.error(f"Add health metric error: {str(e)}")
        flash('Error adding health metric.', 'error')
    
    return redirect(url_for('patient.health_tracking'))

@patient_bp.route('/profile-settings')
@login_required
@role_required(UserRole.PATIENT)
def profile_settings():
    try:
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        patient = Patient.query.filter_by(user_id=user_id).first()
        
        return render_template('profile_setting.html', user=user, patient=patient)
        
    except Exception as e:
        logger.error(f"Profile settings error: {str(e)}")
        flash('Error loading profile settings.', 'error')
        return render_template('profile_setting.html', user=None, patient=None)

@patient_bp.route('/update_profile', methods=['POST'])
@login_required
@role_required(UserRole.PATIENT)
def update_profile():
    try:
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        patient = Patient.query.filter_by(user_id=user_id).first()
        
        # Update user information
        user.first_name = SecurityUtils.sanitize_input(request.form.get('first_name', ''))
        user.last_name = SecurityUtils.sanitize_input(request.form.get('last_name', ''))
        user.phone = request.form.get('phone', '')
        
        # Update patient-specific information
        if request.form.get('date_of_birth'):
            patient.date_of_birth = datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d').date()
        
        patient.gender = request.form.get('gender', '')
        patient.blood_type = request.form.get('blood_type', '')
        patient.emergency_contact_name = SecurityUtils.sanitize_input(request.form.get('emergency_contact_name', ''))
        patient.emergency_contact_phone = request.form.get('emergency_contact_phone', '')
        patient.address = SecurityUtils.sanitize_input(request.form.get('address', ''))
        patient.allergies = SecurityUtils.sanitize_input(request.form.get('allergies', ''))
        
        DatabaseManager.update_db()
        
        flash('Profile updated successfully!', 'success')
        
    except Exception as e:
        logger.error(f"Update profile error: {str(e)}")
        flash('Error updating profile.', 'error')
    
    return redirect(url_for('patient.profile_settings'))

@patient_bp.route('/support-help')
@login_required
@role_required(UserRole.PATIENT)
def support_help():
    return render_template('support_help.html')