from flask import Blueprint
from .auth import auth_bp
from .patients import patients_bp
from .doctors import doctors_bp
from .government import government_bp
from .appointments import appointments_bp

# Create the main v1 blueprint
v1_bp = Blueprint('v1', __name__, url_prefix='/api/v1')

# Register all sub-blueprints
v1_bp.register_blueprint(auth_bp, url_prefix='/auth')
v1_bp.register_blueprint(patients_bp, url_prefix='/patients')
v1_bp.register_blueprint(doctors_bp, url_prefix='/doctors')
v1_bp.register_blueprint(government_bp, url_prefix='/government')
v1_bp.register_blueprint(appointments_bp, url_prefix='/appointments')

# Health check endpoint
@v1_bp.route('/health', methods=['GET'])
def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "Healthcare API"
    }, 200