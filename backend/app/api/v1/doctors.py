from flask import Blueprint, request
from api.deps import APIResponse, token_required, role_required, validate_json
from services.doctor_service import DoctorService
from services.appointment_service import AppointmentService
from services.medical_record_service import MedicalRecordService

doctors_bp = Blueprint('doctors', __name__)

@doctors_bp.route('/profile', methods=['GET'])
@token_required
@role_required(['doctor'])
def get_doctor_profile(current_user_id, current_user_type):
    try:
        doctor = DoctorService.get_doctor_by_id(current_user_id)
        if not doctor:
            return APIResponse.error("Doctor not found", 404)
        
        return APIResponse.success({
            'doctor': doctor
        }, "Profile retrieved successfully")
        
    except Exception as e:
        return APIResponse.error("Failed to retrieve profile", 500)

@doctors_bp.route('/profile', methods=['PUT'])
@token_required
@role_required(['doctor'])
@validate_json()
def update_doctor_profile(data, current_user_id, current_user_type):
    try:
        updated_doctor = DoctorService.update_doctor(current_user_id, data)
        
        return APIResponse.success({
            'doctor': updated_doctor
        }, "Profile updated successfully")
        
    except Exception as e:
        return APIResponse.error("Failed to update profile", 500)

@doctors_bp.route('/appointments', methods=['GET'])
@token_required
@role_required(['doctor'])
def get_doctor_appointments(current_user_id, current_user_type):
    try:
        status = request.args.get('status', 'all')
        date = request.args.get('date')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        appointments = AppointmentService.get_doctor_appointments(
            current_user_id, status, date, page, limit
        )
        
        return APIResponse.success({
            'appointments': appointments['data'],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': appointments['total'],
                'pages': appointments['pages']
            }
        }, "Appointments retrieved successfully")
        
    except Exception as e:
        return APIResponse.error("Failed to retrieve appointments", 500)

@doctors_bp.route('/appointments/<int:appointment_id>/confirm', methods=['PUT'])
@token_required
@role_required(['doctor'])
def confirm_appointment(current_user_id, current_user_type, appointment_id):
    try:
        appointment = AppointmentService.confirm_appointment(appointment_id, current_user_id)
        
        return APIResponse.success({
            'appointment': appointment
        }, "Appointment confirmed successfully")
        
    except ValueError as e:
        return APIResponse.error(str(e), 400)
    except Exception as e:
        return APIResponse.error("Failed to confirm appointment", 500)

@doctors_bp.route('/appointments/<int:appointment_id>/complete', methods=['PUT'])
@token_required
@role_required(['doctor'])
@validate_json(['notes'])
def complete_appointment(data, current_user_id, current_user_type, appointment_id):
    try:
        appointment = AppointmentService.complete_appointment(
            appointment_id, current_user_id, data['notes']
        )
        
        return APIResponse.success({
            'appointment': appointment
        }, "Appointment completed successfully")
        
    except ValueError as e:
        return APIResponse.error(str(e), 400)
    except Exception as e:
        return APIResponse.error("Failed to complete appointment", 500)

@doctors_bp.route('/patients/<int:patient_id>/medical-records', methods=['GET'])
@token_required
@role_required(['doctor'])
def get_patient_medical_records(current_user_id, current_user_type, patient_id):
    try:
        # Verify doctor has access to this patient
        if not DoctorService.has_patient_access(current_user_id, patient_id):
            return APIResponse.error("Access denied", 403)
        
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        record_type = request.args.get('type', 'all')
        
        records = MedicalRecordService.get_patient_records(
            patient_id, record_type, page, limit
        )
        
        return APIResponse.success({
            'records': records['data'],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': records['total'],
                'pages': records['pages']
            }
        }, "Medical records retrieved successfully")
        
    except Exception as e:
        return APIResponse.error("Failed to retrieve medical records", 500)

@doctors_bp.route('/patients/<int:patient_id>/medical-records', methods=['POST'])
@token_required
@role_required(['doctor'])
@validate_json(['record_type', 'title', 'description'])
def add_medical_record(data, current_user_id, current_user_type, patient_id):
    try:
        # Verify doctor has access to this patient
        if not DoctorService.has_patient_access(current_user_id, patient_id):
            return APIResponse.error("Access denied", 403)
        
        data['patient_id'] = patient_id
        data['doctor_id'] = current_user_id
        
        record = MedicalRecordService.create_medical_record(data)
        
        return APIResponse.success({
            'record': record
        }, "Medical record added successfully", 201)
        
    except Exception as e:
        return APIResponse.error("Failed to add medical record", 500)

@doctors_bp.route('/schedule', methods=['GET'])
@token_required
@role_required(['doctor'])
def get_doctor_schedule(current_user_id, current_user_type):
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        schedule = DoctorService.get_doctor_schedule(current_user_id, start_date, end_date)
        
        return APIResponse.success({
            'schedule': schedule
        }, "Schedule retrieved successfully")
        
    except Exception as e:
        return APIResponse.error("Failed to retrieve schedule", 500)

@doctors_bp.route('/schedule', methods=['POST'])
@token_required
@role_required(['doctor'])
@validate_json(['date', 'start_time', 'end_time'])
def set_availability(data, current_user_id, current_user_type):
    try:
        data['doctor_id'] = current_user_id
        
        availability = DoctorService.set_availability(data)
        
        return APIResponse.success({
            'availability': availability
        }, "Availability set successfully", 201)
        
    except ValueError as e:
        return APIResponse.error(str(e), 400)
    except Exception as e:
        return APIResponse.error("Failed to set availability", 500)

@doctors_bp.route('/patients', methods=['GET'])
@token_required
@role_required(['doctor'])
def get_doctor_patients(current_user_id, current_user_type):
    try:
        search = request.args.get('search', '')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        patients = DoctorService.get_doctor_patients(current_user_id, search, page, limit)
        
        return APIResponse.success({
            'patients': patients['data'],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': patients['total'],
                'pages': patients['pages']
            }
        }, "Patients retrieved successfully")
        
    except Exception as e:
        return APIResponse.error("Failed to retrieve patients", 500)

@doctors_bp.route('/stats', methods=['GET'])
@token_required
@role_required(['doctor'])
def get_doctor_stats(current_user_id, current_user_type):
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        stats = DoctorService.get_doctor_statistics(current_user_id, start_date, end_date)
        
        return APIResponse.success({
            'stats': stats
        }, "Statistics retrieved successfully")
        
    except Exception as e:
        return APIResponse.error("Failed to retrieve statistics", 500)