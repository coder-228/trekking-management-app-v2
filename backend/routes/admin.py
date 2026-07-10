from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extensions import db, redis_client
from models import User, Trek, Booking
from werkzeug.security import generate_password_hash
from datetime import datetime
from functools import wraps
import json

admin_bp = Blueprint('admin', __name__)


# ---- DECORATOR ----

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        identity = get_jwt()
        if not identity or identity.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated


# ---- DASHBOARD ----

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@admin_required
def dashboard():
    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role='user').count()
    total_staff = User.query.filter_by(role='staff').count()
    total_bookings = Booking.query.count()
    active_bookings = Booking.query.filter_by(status='Booked').count()

    status_stats = {}
    for status in ['Pending', 'Approved', 'Open', 'Closed', 'Completed']:
        status_stats[status] = Trek.query.filter_by(status=status).count()

    difficulty_stats = {
        'Easy': Trek.query.filter_by(difficulty='Easy').count(),
        'Moderate': Trek.query.filter_by(difficulty='Moderate').count(),
        'Hard': Trek.query.filter_by(difficulty='Hard').count()
    }

    recent_bookings = Booking.query.order_by(
        Booking.booking_date.desc()).limit(5).all()

    return jsonify({
        'total_treks': total_treks,
        'total_users': total_users,
        'total_staff': total_staff,
        'total_bookings': total_bookings,
        'active_bookings': active_bookings,
        'status_stats': status_stats,
        'difficulty_stats': difficulty_stats,
        'recent_bookings': [b.to_dict() for b in recent_bookings]
    }), 200
