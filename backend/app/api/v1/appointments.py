from flask import Blueprint, request
from api.deps import APIResponse, token_required, validate_json
from services.appointment_service import AppointmentService

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/', methods=['GET'])
@token_required
def get_appointments(current_user_id, current_user_type):
    try:
        status = request.args.get('status', 'all')
        date = request.args.get('date')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        if current_user_type == 'patient':
            appointments = AppointmentService.get_patient_appointments(
                current_user_id, status, page, limit
            )
        elif current_user_type == 'doctor':
            appointments = AppointmentService.get_doctor_appointments(
                current_user_id, status, date, page, limit
            )
        else:
            return APIResponse.error("Unauthorized access", 403)
        
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

@appointments_bp.route('/', methods=['POST'])
@token_required
@validate_json(['doctor_id', 'appointment_date', 'appointment_time', 'reason'])
def create_appointment(data, current_user_id, current_user_type):
    try:
        if current_user_type != 'patient':
            return APIResponse.error("Only patients can book appointments", 403)
        
        data['patient_id'] = current_user_id
        
        appointment = AppointmentService.book_appointment(data)
        
        return APIResponse.success({
            'appointment': appointment
        }, "Appointment booked successfully", 201)
        
    except ValueError as e:
        return APIResponse.error(str(e), 400)
    except Exception as e:
        return APIResponse.error("Failed to book appointment", 500)

@appointments_bp.route('/<int:appointment_id>', methods=['GET'])
@token_required
def get_appointment_details(current_user_id, current_user_type, appointment_id):
    try:
        appointment = AppointmentService.get_appointment_by_id(appointment_id)
        
        if not appointment:
            return APIResponse.error("Appointment not found", 404)
        
        # Check if user has access to this appointment
        if (current_user_type == 'patient' and appointment['patient_id'] != current_user_id) or \
           (current_user_type == 'doctor' and appointment['doctor_id'] != current_user_id):
            return APIResponse.error("Access denied", 403)
        
        return APIResponse.success({
            'appointment': appointment
        }, "Appointment details retrieved successfully")
        
    except Exception as e:
        return APIResponse.error("Failed to retrieve appointment details", 500)

@appointments_bp.route('/<int:appointment_id>/cancel', methods=['PUT'])
@token_required
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

@appointments_bp.route('/<int:appointment_id>/reschedule', methods=['PUT'])
@token_required
@validate_json(['new_date', 'new_time'])
def reschedule_appointment(data, current_user_id, current_user_type, appointment_id):
    try:
        appointment = AppointmentService.reschedule_appointment(
            appointment_id, current_user_id, data['new_date'], data['new_time']
        )
        
        return APIResponse.success({
            'appointment': appointment
        }, "Appointment rescheduled successfully")
        
    except ValueError as e:
        return APIResponse.error(str(e), 400)
    except Exception as e:
        return APIResponse.error("Failed to reschedule appointment", 500)

@appointments_bp.route('/<int:appointment_id>/confirm', methods=['PUT'])
@token_required
def confirm_appointment(current_user_id, current_user_type, appointment_id):
    try:
        if current_user_type != 'doctor':
            return APIResponse.error("Only doctors can confirm appointments", 403)
        
        appointment = AppointmentService.confirm_appointment(appointment_id, current_user_id)
        
        return APIResponse.success({
            'appointment': appointment
        }, "Appointment confirmed successfully")
        
    except ValueError as e:
        return APIResponse.error(str(e), 400)
    except Exception as e:
        return APIResponse.error("Failed to confirm appointment", 500)

@appointments_bp.route('/<int:appointment_id>/complete', methods=['PUT'])
@token_required
@validate_json(['notes'])
def complete_appointment(data, current_user_id, current_user_type, appointment_id):
    try:
        if current_user_type != 'doctor':
            return APIResponse.error("Only doctors can complete appointments", 403)
        
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

@appointments_bp.route('/available-slots', methods=['GET'])
@token_required
def get_available_slots(current_user_id, current_user_type):
    try:
        doctor_id = request.args.get('doctor_id', type=int)
        date = request.args.get('date')
        
        if not doctor_id or not date:
            return APIResponse.error("doctor_id and date are required", 400)
        
        slots = AppointmentService.get_available_slots(doctor_id, date)
        
        return APIResponse.success({
            'available_slots': slots,
            'doctor_id': doctor_id,
            'date': date
        }, "Available slots retrieved successfully")
        
    except Exception as e:
        return APIResponse.error("Failed to retrieve available slots", 500)