from .models import db
from .exceptions import DatabaseError
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Database operations utility class"""
    
    @staticmethod
    def init_db(app):
        """Initialize database with Flask app"""
        db.init_app(app)
        
    @staticmethod
    def create_tables():
        """Create all database tables"""
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {str(e)}")
            raise DatabaseError(f"Failed to create database tables: {str(e)}")
    
    @staticmethod
    def drop_tables():
        """Drop all database tables (use with caution)"""
        try:
            db.drop_all()
            logger.info("Database tables dropped")
        except Exception as e:
            logger.error(f"Error dropping database tables: {str(e)}")
            raise DatabaseError(f"Failed to drop database tables: {str(e)}")
    
    @staticmethod
    def save_to_db(obj):
        """Save object to database"""
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving to database: {str(e)}")
            raise DatabaseError(f"Failed to save to database: {str(e)}")
    
    @staticmethod
    def update_db():
        """Commit current database session"""
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating database: {str(e)}")
            raise DatabaseError(f"Failed to update database: {str(e)}")
    
    @staticmethod
    def delete_from_db(obj):
        """Delete object from database"""
        try:
            db.session.delete(obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting from database: {str(e)}")
            raise DatabaseError(f"Failed to delete from database: {str(e)}")
    
    @staticmethod
    def rollback():
        """Rollback current database session"""
        try:
            db.session.rollback()
        except Exception as e:
            logger.error(f"Error rolling back database session: {str(e)}")

def init_sample_data():
    """Initialize database with sample data for development"""
    from .models import User, Patient, Doctor, GovernmentOfficial
    from .security import SecurityUtils
    
    try:
        # Check if sample data already exists
        if User.query.first():
            logger.info("Sample data already exists")
            return
        
        # Create sample users
        sample_users = [
            {
                'email': 'patient@example.com',
                'password': 'Password123!',
                'role': 'patient',
                'first_name': 'John',
                'last_name': 'Doe'
            },
            {
                'email': 'doctor@example.com',
                'password': 'Password123!',
                'role': 'doctor',
                'first_name': 'Dr. Jane',
                'last_name': 'Smith'
            },
            {
                'email': 'gov@example.com',
                'password': 'Password123!',
                'role': 'government',
                'first_name': 'Government',
                'last_name': 'Official'
            }
        ]
        
        for user_data in sample_users:
            # Create user
            user = User(
                email=user_data['email'],
                password_hash=SecurityUtils.hash_password(user_data['password']),
                role=UserRole(user_data['role']),
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                is_verified=True
            )
            db.session.add(user)
            db.session.flush()  # To get the user ID
            
            # Create role-specific profiles
            if user_data['role'] == 'patient':
                patient = Patient(
                    user_id=user.id,
                    date_of_birth=datetime(1990, 1, 1).date(),
                    gender='Male',
                    blood_type='O+',
                    emergency_contact_name='Jane Doe',
                    emergency_contact_phone='1234567890'
                )
                db.session.add(patient)
                
            elif user_data['role'] == 'doctor':
                doctor = Doctor(
                    user_id=user.id,
                    license_number='MD123456',
                    specialization='General Medicine',
                    qualification='MBBS, MD',
                    experience_years=10,
                    hospital_affiliation='City General Hospital',
                    consultation_fee=100.00,
                    is_verified=True
                )
                db.session.add(doctor)
                
            elif user_data['role'] == 'government':
                gov_official = GovernmentOfficial(
                    user_id=user.id,
                    department='Health Ministry',
                    position='Health Data Analyst',
                    employee_id='GOV001',
                    clearance_level='Level 2'
                )
                db.session.add(gov_official)
        
        db.session.commit()
        logger.info("Sample data created successfully")
        
    except Exception as