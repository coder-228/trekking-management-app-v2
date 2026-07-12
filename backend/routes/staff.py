from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extensions import db
from models import User, Trek, Booking
from datetime import datetime
from functools import wraps

staff_bp = Blueprint('staff', __name__)

def staff_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        claims = get_jwt()
        if not claims or claims.get('role') != 'staff':
            return jsonify({'error': 'Staff access required'}), 403
        return f(*args, **kwargs)
    return decorated

@staff_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@staff_required
def dashboard():
    staff_id = int(get_jwt_identity())

    assigned_treks = Trek.query.filter_by(staff_id=staff_id).all()
    total_participants = sum(t.booked_slots for t in assigned_treks)
    open_treks = [t for t in assigned_treks if t.status == 'Open']

    return jsonify({
        'assigned_treks': [t.to_dict() for t in assigned_treks],
        'total_participants': total_participants,
        'open_treks_count': len(open_treks),
        'total_treks': len(assigned_treks)
    }), 200

@staff_bp.route('/treks', methods=['GET'])
@jwt_required()
@staff_required
def get_treks():
    treks = Trek.query.filter_by(staff_id=int(get_jwt_identity())).all()
    return jsonify([t.to_dict() for t in treks]), 200


@staff_bp.route('/treks/<int:trek_id>', methods=['GET'])
@jwt_required()
@staff_required
def get_trek(trek_id):
    staff_id = int(get_jwt_identity())
    trek = Trek.query.get_or_404(trek_id)
    if trek.staff_id != staff_id:
        return jsonify({'error': 'Not authorized for this trek'}), 403

    bookings = Booking.query.filter_by(
        trek_id=trek_id, status='Booked').all()

    return jsonify({
        'trek': trek.to_dict(),
        'bookings': [b.to_dict() for b in bookings]
    }), 200


@staff_bp.route('/treks/<int:trek_id>', methods=['PUT'])
@jwt_required()
@staff_required
def update_trek(trek_id):
    staff_id = int(get_jwt_identity())
    trek = Trek.query.get_or_404(trek_id)
    if trek.staff_id != staff_id:
        return jsonify({'error': 'Not authorized for this trek'}), 403

    data = request.get_json()

    # Staff can only update status and slots
    new_status = data.get('status')
    new_slots = data.get('available_slots')

    if new_status:
        allowed = ['Open', 'Closed', 'Completed']
        if new_status not in allowed:
            return jsonify({
                'error': f'Status must be one of {allowed}'
            }), 400
        trek.status = new_status

    if new_slots is not None:
        slots = int(new_slots)
        booked = trek.booked_slots
        if slots < booked:
            return jsonify({
                'error': f'Slots cannot be less than booked ({booked})'
            }), 400
        trek.available_slots = slots
        if slots > trek.total_slots:
            trek.total_slots = slots

    db.session.commit()
    return jsonify(trek.to_dict()), 200

@staff_bp.route('/treks/<int:trek_id>/participants', methods=['GET'])
@jwt_required()
@staff_required
def get_participants(trek_id):
    staff_id = int(get_jwt_identity())
    trek = Trek.query.get_or_404(trek_id)
    if trek.staff_id != staff_id:
        return jsonify({'error': 'Not authorized'}), 403

    bookings = Booking.query.filter_by(trek_id=trek_id).all()
    return jsonify([b.to_dict() for b in bookings]), 200

@staff_bp.route('/profile', methods=['GET'])
@jwt_required()
@staff_required
def get_profile():
    staff = User.query.get(int(get_jwt_identity()))
    if not staff:
        return jsonify({'error': 'Staff not found'}), 404
    return jsonify(staff.to_dict()), 200
