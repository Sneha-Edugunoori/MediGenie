from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from .models import db, User, Patient, Doctor, Appointment, MedicalRecord, AppointmentStatus
from .permissions import login_required, role_required, UserRole
from .security import SecurityUtils
from .exceptions import ValidationError, ResourceNotFoundError
from .database import DatabaseManager
from datetime import datetime, timedelta
import logging

doctor_bp = Blueprint('doctor', __name__)
logger = logging.getLogger(__name__)

@doctor_bp.route('/doctor_dashboard')
@login_required
@role_required(UserRole.DOCTOR)
def doctor_dashboard():
    try:
        user_id = session.get('user_id')
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        
        if not doctor:
            flash('Doctor profile not found.', 'error')
            return redirect(url_for('auth.logout'))
        
        # Get today's appointments
        today = datetime.utcnow().date()
        today_appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            db.func.date(Appointment.appointment_date) == today,
            Appointment.status.in_([AppointmentStatus.SCHEDULED, AppointmentStatus.CONFIRMED])
        ).order_by(Appointment.appointment_date.asc()).all()
        
        # Get upcoming appointments (next 7 days)
        next_week = today + timedelta(days=7)
        upcoming_appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.appointment_date > datetime.utcnow(),
            db.func.date(Appointment.appointment_date) <= next_week,
            Appointment.status.in_([AppointmentStatus.SCHEDULED, AppointmentStatus.CONFIRMED])
        ).order_by(Appointment.appointment_date.asc()).limit(10).all()
        
        # Get recent patients
        recent_patients = db.session.query(Patient).join(Appointment)\
            .filter(Appointment.doctor_id == doctor.id)\
            .order_by(Appointment.appointment_date.desc())\
            .distinct().limit(5).all()
        
        dashboard_data = {
            'doctor': doctor,
            'today_appointments': today_appointments,
            'upcoming_appointments': upcoming_appointments,
            'recent_patients': recent_patients,
            'total_patients': db.session.query(Patient.id).join(Appointment)
                .filter(Appointment.doctor_id == doctor.id).distinct().count(),
            'total_appointments': Appointment.query.filter_by(doctor_id=doctor.id).count()
        }
        
        return render_template('doctor_dashboard.html', data=dashboard_data)
        
    except Exception as e:
        logger.error(f"Doctor appointments error: {str(e)}")
        flash('Error loading appointments.', 'error')
        return render_template('doctor_appointments.html', appointments=[], status_filter='all', date_filter='all')

@doctor_bp.route('/update_appointment_status/<int:appointment_id>', methods=['POST'])
@login_required
@role_required(UserRole.DOCTOR)
def update_appointment_status(appointment_id):
    try:
        user_id = session.get('user_id')
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        
        appointment = Appointment.query.filter_by(id=appointment_id, doctor_id=doctor.id).first()
        if not appointment:
            raise ResourceNotFoundError("Appointment not found")
        
        new_status = request.form.get('status')
        if new_status:
            appointment.status = AppointmentStatus(new_status)
            appointment.notes = SecurityUtils.sanitize_input(request.form.get('notes', ''))
            DatabaseManager.update_db()
            
            flash('Appointment status updated successfully!', 'success')
        
    except Exception as e:
        logger.error(f"Update appointment status error: {str(e)}")
        flash('Error updating appointment status.', 'error')
    
    return redirect(url_for('doctor.doctor_appointments'))

@doctor_bp.route('/patient_records/<int:patient_id>')
@login_required
@role_required(UserRole.DOCTOR)
def patient_records(patient_id):
    try:
        user_id = session.get('user_id')
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        
        patient = Patient.query.get_or_404(patient_id)
        
        # Get patient's medical records
        records = MedicalRecord.query.filter_by(patient_id=patient_id)\
            .order_by(MedicalRecord.record_date.desc()).all()
        
        # Get patient's health metrics
        health_metrics = HealthMetric.query.filter_by(patient_id=patient_id)\
            .order_by(HealthMetric.recorded_at.desc()).limit(20).all()
        
        return render_template('patient_records.html', 
                             patient=patient, 
                             records=records,
                             health_metrics=health_metrics)
        
    except Exception as e:
        logger.error(f"Patient records error: {str(e)}")
        flash('Error loading patient records.', 'error')
        return redirect(url_for('doctor.doctor_dashboard'))

@doctor_bp.route('/add_medical_record', methods=['POST'])
@login_required
@role_required(UserRole.DOCTOR)
def add_medical_record():
    try:
        user_id = session.get('user_id')
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        
        patient_id = request.form.get('patient_id')
        appointment_id = request.form.get('appointment_id')
        diagnosis = SecurityUtils.sanitize_input(request.form.get('diagnosis', ''))
        treatment = SecurityUtils.sanitize_input(request.form.get('treatment', ''))
        prescription = SecurityUtils.sanitize_input(request.form.get('prescription', ''))
        notes = SecurityUtils.sanitize_input(request.form.get('notes', ''))
        
        if not all([patient_id, diagnosis]):
            raise ValidationError("Patient ID and diagnosis are required")
        
        # Verify patient exists and doctor has access
        patient = Patient.query.get(patient_id)
        if not patient:
            raise ResourceNotFoundError("Patient not found")
        
        # Create medical record
        record = MedicalRecord(
            patient_id=patient_id,
            doctor_id=doctor.id,
            appointment_id=appointment_id if appointment_id else None,
            diagnosis=diagnosis,
            treatment=treatment,
            prescription=prescription,
            notes=notes
        )
        
        DatabaseManager.save_to_db(record)
        
        flash('Medical record added successfully!', 'success')
        return redirect(url_for('doctor.patient_records', patient_id=patient_id))
        
    except ValidationError as e:
        flash(str(e), 'error')
    except Exception as e:
        logger.error(f"Add medical record error: {str(e)}")
        flash('Error adding medical record.', 'error')
    
    return redirect(url_for('doctor.doctor_dashboard'))

@doctor_bp.route('/doctor_profile')
@login_required
@role_required(UserRole.DOCTOR)
def doctor_profile():
    try:
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        
        return render_template('doctor_profile.html', user=user, doctor=doctor)
        
    except Exception as e:
        logger.error(f"Doctor profile error: {str(e)}")
        flash('Error loading profile.', 'error')
        return render_template('doctor_profile.html', user=None, doctor=None)

@doctor_bp.route('/update_doctor_profile', methods=['POST'])
@login_required
@role_required(UserRole.DOCTOR)
def update_doctor_profile():
    try:
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        
        # Update user information
        user.first_name = SecurityUtils.sanitize_input(request.form.get('first_name', ''))
        user.last_name = SecurityUtils.sanitize_input(request.form.get('last_name', ''))
        user.phone = request.form.get('phone', '')
        
        # Update doctor-specific information
        doctor.specialization = SecurityUtils.sanitize_input(request.form.get('specialization', ''))
        doctor.qualification = SecurityUtils.sanitize_input(request.form.get('qualification', ''))
        doctor.experience_years = int(request.form.get('experience_years', 0))
        doctor.hospital_affiliation = SecurityUtils.sanitize_input(request.form.get('hospital_affiliation', ''))
        doctor.consultation_fee = float(request.form.get('consultation_fee', 0))
        
        DatabaseManager.update_db()
        
        flash('Profile updated successfully!', 'success')
        
    except Exception as e:
        logger.error(f"Update doctor profile error: {str(e)}")
        flash('Error updating profile.', 'error')
    
    return redirect(url_for('doctor.doctor_profile')) Exception as e:
        logger.error(f"Doctor dashboard error: {str(e)}")
        flash('Error loading dashboard.', 'error')
        return render_template('doctor_dashboard.html', data={})

@doctor_bp.route('/doctor_appointments')
@login_required
@role_required(UserRole.DOCTOR)
def doctor_appointments():
    try:
        user_id = session.get('user_id')
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        
        # Get filter parameters
        status_filter = request.args.get('status', 'all')
        date_filter = request.args.get('date', 'all')
        
        # Base query
        query = Appointment.query.filter_by(doctor_id=doctor.id)
        
        # Apply status filter
        if status_filter != 'all':
            query = query.filter(Appointment.status == AppointmentStatus(status_filter))
        
        # Apply date filter
        if date_filter == 'today':
            today = datetime.utcnow().date()
            query = query.filter(db.func.date(Appointment.appointment_date) == today)
        elif date_filter == 'upcoming':
            query = query.filter(Appointment.appointment_date > datetime.utcnow())
        elif date_filter == 'past':
            query = query.filter(Appointment.appointment_date < datetime.utcnow())
        
        appointments_list = query.order_by(Appointment.appointment_date.desc()).all()
        
        return render_template('doctor_appointments.html', 
                             appointments=appointments_list,
                             status_filter=status_filter,
                             date_filter=date_filter)
        
    except