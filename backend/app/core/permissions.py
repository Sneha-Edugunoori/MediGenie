from enum import Enum
from typing import List, Dict, Set
from functools import wraps
from flask import request
from core.exceptions import AuthorizationError

class UserRole(Enum):
    """User role enumeration"""
    PATIENT = "patient"
    DOCTOR = "doctor"
    GOVERNMENT = "government"
    ADMIN = "admin"

class Permission(Enum):
    """Permission enumeration"""
    # Patient permissions
    VIEW_OWN_PROFILE = "view_own_profile"
    EDIT_OWN_PROFILE = "edit_own_profile"
    BOOK_APPOINTMENT = "book_appointment"
    VIEW_OWN_APPOINTMENTS = "view_own_appointments"
    CANCEL_OWN_APPOINTMENT = "cancel_own_appointment"
    VIEW_OWN_MEDICAL_RECORDS = "view_own_medical_records"
    ADD_HEALTH_METRICS = "add_health_metrics"
    VIEW_DOCTORS = "view_doctors"
    
    # Doctor permissions
    VIEW_DOCTOR_PROFILE = "view_doctor_profile"
    EDIT_DOCTOR_PROFILE = "edit_doctor_profile"
    VIEW_DOCTOR_APPOINTMENTS = "view_doctor_appointments"
    CONFIRM_APPOINTMENT = "confirm_appointment"
    COMPLETE_APPOINTMENT = "complete_appointment"
    VIEW_PATIENT_RECORDS = "view_patient_records"
    CREATE_MEDICAL_RECORD = "create_medical_record"
    EDIT_MEDICAL_RECORD = "edit_medical_record"
    SET_AVAILABILITY = "set_availability"
    VIEW_DOCTOR_PATIENTS = "view_doctor_patients"
    VIEW_DOCTOR_STATS = "view_doctor_stats"
    
    # Government permissions
    VERIFY_DOCTORS = "verify_doctors"
    VIEW_ALL_DOCTORS = "view_all_doctors"
    VIEW_ANALYTICS = "view_analytics"
    GENERATE_REPORTS = "generate_reports"
    VIEW_HEALTH_ALERTS = "view_health_alerts"
    MANAGE_POLICIES = "manage_policies"
    VIEW_AUDIT_LOGS = "view_audit_logs"
    VIEW_SYSTEM_STATS = "view_system_stats"
    
    # Admin permissions (future use)
    MANAGE_USERS = "manage_users"
    SYSTEM_ADMIN = "system_admin"

class RolePermissionMatrix:
    """Defines which roles have which permissions"""
    
    ROLE_PERMISSIONS = {
        UserRole.PATIENT: {
            Permission.VIEW_OWN_PROFILE,
            Permission.EDIT_OWN_PROFILE,
            Permission.BOOK_APPOINTMENT,
            Permission.VIEW_OWN_APPOINTMENTS,
            Permission.CANCEL_OWN_APPOINTMENT,
            Permission.VIEW_OWN_MEDICAL_RECORDS,
            Permission.ADD_HEALTH_METRICS,
            Permission.VIEW_DOCTORS,
        },
        
        UserRole.DOCTOR: {
            Permission.VIEW_DOCTOR_PROFILE,
            Permission.EDIT_DOCTOR_PROFILE,
            Permission.VIEW_DOCTOR_APPOINTMENTS,
            Permission.CONFIRM_APPOINTMENT,
            Permission.COMPLETE_APPOINTMENT,
            Permission.VIEW_PATIENT_RECORDS,
            Permission.CREATE_MEDICAL_RECORD,
            Permission.EDIT_MEDICAL_RECORD,
            Permission.SET_AVAILABILITY,
            Permission.VIEW_DOCTOR_PATIENTS,
            Permission.VIEW_DOCTOR_STATS,
        },
        
        UserRole.GOVERNMENT: {
            Permission.VERIFY_DOCTORS,
            Permission.VIEW_ALL_DOCTORS,
            Permission.VIEW_ANALYTICS,
            Permission.GENERATE_REPORTS,
            Permission.VIEW_HEALTH_ALERTS,
            Permission.MANAGE_POLICIES,
            Permission.VIEW_AUDIT_LOGS,
            Permission.VIEW_SYSTEM_STATS,
        },
        
        UserRole.ADMIN: {
            # Admin has all permissions
            perm for perm in Permission
        }
    }
    
    @classmethod
    def get_permissions(cls, role: UserRole) -> Set[Permission]:
        """Get permissions for a role"""
        return cls.ROLE_PERMISSIONS.get(role, set())
    
    @classmethod
    def has_permission(cls, role: UserRole, permission: Permission) -> bool:
        """Check if role has specific permission"""
        role_permissions = cls.get_permissions(role)
        return permission in role_permissions

class PermissionChecker:
    """Permission checking utilities"""
    
    @staticmethod
    def require_permission(permission: Permission):
        """Decorator to require specific permission"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # This assumes token_required decorator has already run
                # and set current_user_type in the function arguments
                if 'current_user_type' not in kwargs and len(args) >= 2:
                    user_type = args[1]  # Assuming second arg is user_type
                else:
                    user_type = kwargs.get('current_user_type')
                
                if not user_type:
                    raise AuthorizationError("User type not found")
                
                try:
                    role = UserRole(user_type)
                except ValueError:
                    raise AuthorizationError("Invalid user role")
                
                if not RolePermissionMatrix.has_permission(role, permission):
                    raise AuthorizationError(f"Permission {permission.value} required")
                
                return f(*args, **kwargs)
            return decorated_function
        return decorator
    
    @staticmethod
    def check_resource_access(user_id: int, user_type: str, resource_owner_id: int, 
                            resource_type: str) -> bool:
        """Check if user can access specific resource"""
        role = UserRole(user_type)
        
        # Users can always access their own resources
        if user_id == resource_owner_id:
            return True
        
        # Doctors can access patient resources if they have a relationship
        if role == UserRole.DOCTOR and resource_type == "patient":
            # This would check if doctor has treated this patient
            return True  # Simplified - implement proper logic in service layer
        
        # Government users can access aggregated data but not individual records
        if role == UserRole.GOVERNMENT and resource_type in ["analytics", "reports"]:
            return True
        
        return False

class DataAccessControl:
    """Data access control utilities"""
    
    @staticmethod
    def filter_sensitive_data(data: Dict, user_role: UserRole) -> Dict:
        """Filter sensitive data based on user role"""
        if user_role == UserRole.PATIENT:
            # Patients see their own full data
            return data
        
        elif user_role == UserRole.DOCTOR:
            # Doctors don't see certain sensitive patient info
            sensitive_fields = ['ssn', 'insurance_details', 'emergency_contacts']
            return {k: v for k, v in data.items() if k not in sensitive_fields}
        
        elif user_role == UserRole.GOVERNMENT:
            # Government sees only aggregated/anonymized data
            public_fields = ['id', 'age', 'gender', 'location', 'diagnosis_codes']
            return {k: v for k, v in data.items() if k in public_fields}
        
        return {}
    
    @staticmethod
    def anonymize_patient_data(patient_data: Dict) -> Dict:
        """Anonymize patient data for government/research use"""
        anonymized = patient_data.copy()
        
        # Remove direct identifiers
        identifiers = ['first_name', 'last_name', 'email', 'phone', 'address', 'ssn']
        for identifier in identifiers:
            anonymized.pop(identifier, None)
        
        # Replace with anonymous ID
        if 'id' in anonymized:
            anonymized['anonymous_id'] = f"ANON_{hash(str(anonymized['id'])) % 100000}"
            anonymized.pop('id')
        
        return anonymized