class HealthcareException(Exception):
    """Base exception class for healthcare application"""
    def __init__(self, message, status_code=500, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        return {
            'error': self.__class__.__name__,
            'message': self.message,
            'payload': self.payload
        }

class ValidationError(HealthcareException):
    """Raised when input validation fails"""
    def __init__(self, message, field=None):
        super().__init__(message, status_code=400)
        self.field = field

class AuthenticationError(HealthcareException):
    """Raised when authentication fails"""
    def __init__(self, message="Authentication failed"):
        super().__init__(message, status_code=401)

class AuthorizationError(HealthcareException):
    """Raised when user lacks required permissions"""
    def __init__(self, message="Insufficient permissions"):
        super().__init__(message, status_code=403)

class NotFoundError(HealthcareException):
    """Raised when requested resource is not found"""
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)

class ConflictError(HealthcareException):
    """Raised when there's a conflict (e.g., duplicate email)"""
    def __init__(self, message="Resource conflict"):
        super().__init__(message, status_code=409)

class BusinessLogicError(HealthcareException):
    """Raised when business rules are violated"""
    def __init__(self, message="Business logic error"):
        super().__init__(message, status_code=422)

# Specific healthcare exceptions
class PatientNotFoundError(NotFoundError):
    def __init__(self, patient_id):
        super().__init__(f"Patient with ID {patient_id} not found")

class DoctorNotFoundError(NotFoundError):
    def __init__(self, doctor_id):
        super().__init__(f"Doctor with ID {doctor_id} not found")

class AppointmentNotFoundError(NotFoundError):
    def __init__(self, appointment_id):
        super().__init__(f"Appointment with ID {appointment_id} not found")

class DoctorNotVerifiedError(BusinessLogicError):
    def __init__(self, doctor_id):
        super().__init__(f"Doctor with ID {doctor_id} is not verified")

class AppointmentConflictError(ConflictError):
    def __init__(self, message="Appointment time conflict"):
        super().__init__(message)

class InvalidAppointmentTimeError(ValidationError):
    def __init__(self, message="Invalid appointment time"):
        super().__init__(message)

class MedicalRecordAccessError(AuthorizationError):
    def __init__(self, message="Access to medical record denied"):
        super().__init__(message)

class InvalidLicenseError(ValidationError):
    def __init__(self, license_number):
        super().__init__(f"Invalid medical license number: {license_number}")

class RateLimitExceededError(HealthcareException):
    def __init__(self, message="Rate limit exceeded"):
        super().__init__(message, status_code=429)

class DatabaseError(HealthcareException):
    """Raised when database operations fail"""
    def __init__(self, message="Database operation failed"):
        super().__init__(message, status_code=500)

class EmailSendError(HealthcareException):
    """Raised when email sending fails"""
    def __init__(self, message="Failed to send email"):
        super().__init__(message, status_code=500)

class FileUploadError(HealthcareException):
    """Raised when file upload fails"""
    def __init__(self, message="File upload failed"):
        super().__init__(message, status_code=400)