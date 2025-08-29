from flask import Blueprint, request
from api.deps import APIResponse, token_required, role_required, validate_json
from services.patient_service import PatientService
from services.appointment_service import AppointmentService
from services.medical_record_service import MedicalRecordService

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/profile', methods=['GET'])
@token_required
@role_required(['patient'])
def get_patient_profile(current_user_id, current_user_type):
    try:
        patient = PatientService.get_patient_by_id(current_user_id)
        if not patient:
            return APIResponse.error("Patient not found", 404)
        
        return APIResponse.success({
            'patient': patient
        }, "Profile retrieved successfully")
        
    except Exception as e:
        return APIResponse.error("Failed to retrieve profile", 500)

@patients_bp.route('/profile', methods=['PUT'])
@token_required
@role_required(['patient'])
@validate_json()
def update_patient_profile(data, current_user_id, current_user_type):
    try:
        # Update patient profile
        updated_patient = PatientService.update_patient(current_user_id, data)
        
        return APIResponse.success({
            'patient': updated_patient
        }, "Profile updated successfully")
        
    except Exception as e:
        return APIResponse.error("Failed to update profile", 500)

@patients_bp.route('/appointments', methods=['GET'])
@token_required
@role_required(['patient'])
def get_patient_appointments(current_user_id, current_user_type):
    try:
        status = request.args.get('status', 'all')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        appointments = AppointmentService.get_patient_appointments(
            current_user_id, status, page, limit
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

@patients_bp.route('/appointments', methods=['POST'])
@token_required
@role_required(['patient'])
@validate_json(['doctor_id', 'appointment_date', 'appointment_time', 'reason'])
def book_appointment(data, current_user_id, current_user_type):
    try:
        data['patient_id'] = current_user_id
        
        appointment = AppointmentService.book_appointment(data)
        
        return APIResponse.success({
            'appointment': appointment
        }, "Appointment booked successfully", 201)
        
    except ValueError as e:
        return APIResponse.error(str(e), 400)
    except Exception as e:
        return APIResponse.error("Failed to book appointment", 500)

@patients_bp.route('/appointments/<int:appointment_id>/cancel', methods=['PUT'])
@token_required
@role_required(['patient'])
def cancel_appointment(current_user_id, current_user_type, appointment_id):
    try:
        appointment = AppointmentService.cancel_appointment(appointment_id, current_user_id)
        
        return APIResponse.success({
            'appointment': appointment
        }, "Appointment cancelled successfully")
        
    except ValueError as e:
        return APIResponse.error(str(e), 400)
    except Exception as e:
        return APIResponse.error("Failed to cancel appointment", 500)

@patients_bp.route('/medical-records', methods=['GET'])
@token_required
@role_required(['patient'])
def get_medical_records(current_user_id, current_user_type):
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        record_type = request.args.get('type', 'all')
        
        records = MedicalRecordService.get_patient_records(
            current_user_id, record_type, page, limit
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

@patients_bp.route('/health-metrics', methods=['GET'])
@token_required
@role_required(['patient'])
def get_health_metrics(current_user_id, current_user_type):
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        metric_type = request.args.get('type', 'all')
        
        metrics = PatientService.get_health_metrics(
            current_user_id, start_date, end_date, metric_type
        )
        
        return APIResponse.success({
            'metrics': metrics
        }, "Health metrics retrieved successfully")
        
    except Exception as e:
        return APIResponse.error("Failed to retrieve health metrics", 500)

@patients_bp.route('/health-metrics', methods=['POST'])
@token_required
@role_required(['patient'])
@validate_json(['metric_type', 'value', 'recorded_date'])
def add_health_metric(data, current_user_id, current_user_type):
    try:
        data['patient_id'] = current_user_id
        
        metric = PatientService.add_health_metric(data)
        
        return APIResponse.success({
            'metric': metric
        }, "Health metric added successfully", 201)
        
    except Exception as e:
        return APIResponse.error("Failed to add health metric", 500)

@patients_bp.route('/doctors', methods=['GET'])
@token_required
@role_required(['patient'])
def get_available_doctors(current_user_id, current_user_type):
    try:
        specialization = request.args.get('specialization')
        location = request.args.get('location')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        doctors = PatientService.get_available_doctors(
            specialization, location, page, limit
        )
        
        return APIResponse.success({
            'doctors': doctors['data'],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': doctors['total'],
                'pages': doctors['pages']
            }
        }, "Doctors retrieved successfully")
        
    except Exception as e:
        return APIResponse.error("Failed to retrieve doctors", 500)