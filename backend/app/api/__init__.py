from flask import Blueprint
from .v1 import v1_bp

# Create the main API blueprint
api_bp = Blueprint('api', __name__)

# Register version blueprints
api_bp.register_blueprint(v1_bp)

# Global API routes (if any)
@api_bp.route('/', methods=['GET'])
def api_info():
    return {
        "message": "Healthcare Management System API",
        "version": "1.0.0",
        "available_versions": ["v1"],
        "documentation": "/api/v1/docs"
    }, 200