from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from .models import db, User, Patient, Doctor, Appointment, MedicalRecord, HealthMetric, AppointmentStatus, UserRole
from .permissions import login_required, role_required
from .exceptions import ValidationError, ResourceNotFoundError
from datetime import datetime, timedelta
from sqlalchemy import func, desc
import logging

government_bp = Blueprint('government', __name__)
logger = logging.getLogger(__name__)

@government_bp.route('/government_dashboard')
@login_required
@role_required(UserRole.GOVERNMENT)
def government_dashboard():
    try:
        # Get overview statistics
        total_patients = Patient.query.count()
        total_doctors = Doctor.query.count()
        total_appointments = Appointment.query.count()
        total_records = MedicalRecord.query.count()
        
        # Get recent statistics (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        recent_registrations = User.query.filter(
            User.created_at >= thirty_days_ago
        ).count()
        
        recent_appointments = Appointment.query.filter(
            Appointment.created_at >= thirty_days_ago
        ).count()
        
        # Get appointment status distribution
        appointment_stats = db.session.query(
            Appointment.status,
            func.count(Appointment.id).label('count')
        ).group_by(Appointment.status).all()
        
        # Get top diagnoses (last 6 months)
        six_months_ago = datetime.utcnow() - timedelta(days=180)
        top_diagnoses = db.session.query(
            MedicalRecord.diagnosis,
            func.count(MedicalRecord.id).label('count')
        ).filter(
            MedicalRecord.record_date >= six_months_ago,
            MedicalRecord.diagnosis.isnot(None),
            MedicalRecord.diagnosis != ''
        ).group_by(MedicalRecord.diagnosis)\
         .order_by(desc('count')).limit(10).all()
        
        # Get doctor verification status
        verified_doctors = Doctor.query.filter_by(is_verified=True).count()
        pending_doctors = Doctor.query.filter_by(is_verified=False).count()
        
        dashboard_data = {
            'total_patients': total_patients,
            'total_doctors': total_doctors,
            'total_appointments': total_appointments,
            'total_records': total_records,
            'recent_registrations': recent_registrations,
            'recent_appointments': recent_appointments,
            'appointment_stats': appointment_stats,
            'top_diagnoses': top_diagnoses,
            'verified_doctors': verified_doctors,
            'pending_doctors': pending_doctors
        }
        
        return render_template('government_dashboard.html', data=dashboard_data)
        
    except Exception as e:
        logger.error(f"Government dashboard error: {str(e)}")
        flash('Error loading dashboard.', 'error')
        return render_template('government_dashboard.html', data={})

@government_bp.route('/health_analytics')
@login_required
@role_required(UserRole.GOVERNMENT)
def health_analytics():
    try:
        # Get health metrics statistics
        metric_stats = db.session.query(
            HealthMetric.metric_type,
            func.count(HealthMetric.id).label('count'),
            func.avg(func.cast(HealthMetric.value, db.Float)).label('avg_value')
        ).group_by(HealthMetric.metric_type).all()
        
        # Get monthly health trends (last 12 months)
        twelve_months_ago = datetime.utcnow() - timedelta(days=365)
        monthly_trends = db.session.query(
            func.date_trunc('month', HealthMetric.recorded_at).label('month'),
            HealthMetric.metric_type,
            func.count(HealthMetric.id).label('count')
        ).filter(
            HealthMetric.recorded_at >= twelve_months_ago
        ).group_by('month', HealthMetric.metric_type)\
         .order_by('month').all()
        
        # Get age distribution of patients
        age_distribution = db.session.query(
            func.date_part('year', func.age(Patient.date_of_birth)).label('age_group'),
            func.count(Patient.id).label('count')
        ).filter(Patient.date_of_birth.isnot(None))\
         .group_by('age_group').all()
        
        # Group ages into ranges
        age_ranges = {'0-18': 0, '19-35': 0, '36-50': 0, '51-65': 0, '65+': 0}
        for age, count in age_distribution:
            if age <= 18:
                age_ranges['0-18'] += count
            elif age <= 35:
                age_ranges['19-35'] += count
            elif age <= 50:
                age_ranges['36-50'] += count
            elif age <= 65:
                age_ranges['51-65'] += count
            else:
                age_ranges['65+'] += count
        
        analytics_data = {
            'metric_stats': metric_stats,
            'monthly_trends': monthly_trends,
            'age_ranges': age_ranges
        }
        
        return render_template('health_analytics.html', data=analytics_data)
        
    except Exception as e:
        logger.error(f"Health analytics error: {str(e)}")
        flash('Error loading analytics.', 'error')
        return render_template('health_analytics.html', data={})

@government_bp.route('/disease_surveillance')
@login_required
@role_required(UserRole.GOVERNMENT)
def disease_surveillance():
    try:
        # Get disease trend data from medical records
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)
        
        # Recent diagnoses (last 30 days)
        recent_diagnoses = db.session.query(
            MedicalRecord.diagnosis,
            func.count(MedicalRecord.id).label('recent_count')
        ).filter(
            MedicalRecord.record_date >= thirty_days_ago,
            MedicalRecord.diagnosis.isnot(None),
            MedicalRecord.diagnosis != ''
        ).group_by(MedicalRecord.diagnosis)\
         .order_by(desc('recent_count')).limit(20).all()
        
        # Previous period diagnoses (30-90 days ago)
        previous_diagnoses = db.session.query(
            MedicalRecord.diagnosis,
            func.count(MedicalRecord.id).label('previous_count')
        ).filter(
            MedicalRecord.record_date >= ninety_days_ago,
            MedicalRecord.record_date < thirty_days_ago,
            MedicalRecord.diagnosis.isnot(None),
            MedicalRecord.diagnosis != ''
        ).group_by(MedicalRecord.diagnosis).all()
        
        # Calculate trend changes
        previous_dict = {diag: count for diag, count in previous_diagnoses}
        trend_data = []
        
        for diagnosis, recent_count in recent_diagnoses:
            previous_count = previous_dict.get(diagnosis, 0)
            if previous_count > 0:
                change_percent = ((recent_count - previous_count) / previous_count) * 100
            else:
                change_percent = 100 if recent_count > 0 else 0
            
            trend_data.append({
                'diagnosis': diagnosis,
                'recent_count': recent_count,
                'previous_count': previous_count,
                'change_percent': round(change_percent, 1)
            })
        
        # Get geographic distribution (would need location data)
        # For now, we'll use hospital affiliations as a proxy
        location_stats = db.session.query(
            Doctor.hospital_affiliation,
            func.count(MedicalRecord.id).label('cases')
        ).join(MedicalRecord).filter(
            MedicalRecord.record_date >= thirty_days_ago,
            Doctor.hospital_affiliation.isnot(None)
        ).group_by(Doctor.hospital_affiliation).all()
        
        surveillance_data = {
            'trend_data': trend_data,
            'location_stats': location_stats,
            'total_recent_cases': sum([data['recent_count'] for data in trend_data])
        }
        
        return render_template('disease_surveillance.html', data=surveillance_data)
        
    except Exception as e:
        logger.error(f"Disease surveillance error: {str(e)}")
        flash('Error loading surveillance data.', 'error')
        return render_template('disease_surveillance.html', data={})

@government_bp.route('/generate_report')
@login_required
@role_required(UserRole.GOVERNMENT)
def generate_report():
    try:
        report_type = request.args.get('type', 'monthly')
        
        if report_type == 'monthly':
            # Generate monthly health report
            start_date = datetime.utcnow().replace(day=1)
            end_date = datetime.utcnow()
        elif report_type == 'quarterly':
            # Generate quarterly report
            current_quarter = ((datetime.utcnow().month - 1) // 3) + 1
            start_month = (current_quarter - 1) * 3 + 1
            start_date = datetime.utcnow().replace(month=start_month, day=1)
            end_date = datetime.utcnow()
        else:
            # Default to monthly
            start_date = datetime.utcnow().replace(day=1)
            end_date = datetime.utcnow()
        
        # Collect report data
        report_data = {
            'period': f"{start_date.strftime('%B %Y')} to {end_date.strftime('%B %Y')}",
            'new_patients': Patient.query.join(User).filter(
                User.created_at >= start_date,
                User.created_at <= end_date
            ).count(),
            'new_doctors': Doctor.query.join(User).filter(
                User.created_at >= start_date,
                User.created_at <= end_date
            ).count(),
            'total_appointments': Appointment.query.filter(
                Appointment.appointment_date >= start_date,
                Appointment.appointment_date <= end_date
            ).count(),
            'completed_appointments': Appointment.query.filter(
                Appointment.appointment_date >= start_date,
                Appointment.appointment_date <= end_date,
                Appointment.status == AppointmentStatus.COMPLETED
            ).count(),
            'top_diagnoses': db.session.query(
                MedicalRecord.diagnosis,
                func.count(MedicalRecord.id).label('count')
            ).filter(
                MedicalRecord.record_date >= start_date,
                MedicalRecord.record_date <= end_date,
                MedicalRecord.diagnosis.isnot(None),
                MedicalRecord.diagnosis != ''
            ).group_by(MedicalRecord.diagnosis)\
             .order_by(desc('count')).limit(10).all()
        }
        
        return render_template('health_report.html', data=report_data, report_type=report_type)
        
    except Exception as e:
        logger.error(f"Generate report error: {str(e)}")
        flash('Error generating report.', 'error')
        return redirect(url_for('government.government_dashboard'))

@government_bp.route('/api/health_metrics')
@login_required
@role_required(UserRole.GOVERNMENT)
def api_health_metrics():
    """API endpoint for health metrics data"""
    try:
        metric_type = request.args.get('type', 'all')
        days = int(request.args.get('days', 30))
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        query = HealthMetric.query.filter(HealthMetric.recorded_at >= start_date)
        
        if metric_type != 'all':
            query = query.filter(HealthMetric.metric_type == metric_type)
        
        metrics = query.order_by(HealthMetric.recorded_at.asc()).all()
        
        # Format data for charts
        chart_data = []
        for metric in metrics:
            try:
                value = float(metric.value)
                chart_data.append({
                    'date': metric.recorded_at.strftime('%Y-%m-%d'),
                    'value': value,
                    'type': metric.metric_type
                })
            except ValueError:
                # Skip non-numeric values
                continue
        
        return jsonify({
            'success': True,
            'data': chart_data
        })
        
    except Exception as e:
        logger.error(f"API health metrics error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error fetching health metrics'
        }), 500