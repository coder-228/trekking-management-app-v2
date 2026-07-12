from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extensions import db, redis_client
from models import User, Trek, Booking
from datetime import datetime
from functools import wraps
import json

user_bp = Blueprint('user', __name__)

def user_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        identity = get_jwt()
        if not identity or identity.get('role') != 'user':
            return jsonify({'error': 'User access required'}), 403
        return f(*args, **kwargs)
    return decorated

@user_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@user_required
def dashboard():
    user_id = int(get_jwt_identity())

    my_bookings = Booking.query.filter_by(
        user_id=user_id).order_by(
        Booking.booking_date.desc()).all()

    active_bookings = [b for b in my_bookings if b.status == 'Booked']
    completed = [b for b in my_bookings if b.status == 'Completed']

    # Get open treks from cache
    cached = redis_client.get('open_treks')
    if cached:
        open_treks = json.loads(cached)
    else:
        treks = Trek.query.filter(
            Trek.status.in_(['Open', 'Approved'])
        ).order_by(Trek.start_date).limit(6).all()
        open_treks = [t.to_dict() for t in treks]
        redis_client.setex('open_treks', 300, json.dumps(open_treks))

    return jsonify({
        'active_bookings': [b.to_dict() for b in active_bookings],
        'completed_count': len(completed),
        'total_bookings': len(my_bookings),
        'open_treks': open_treks
    }), 200

@user_bp.route('/treks', methods=['GET'])
@jwt_required()
@user_required
def get_treks():
    search = request.args.get('search', '')
    difficulty = request.args.get('difficulty', '')
    location = request.args.get('location', '')
    max_price = request.args.get('max_price', '')

    # Only use cache for unfiltered requests
    if not search and not difficulty and not location and not max_price:
        cached = redis_client.get('open_treks')
        if cached:
            return jsonify(json.loads(cached)), 200

    query = Trek.query.filter(Trek.status.in_(['Open', 'Approved']))

    if search:
        query = query.filter(
            Trek.name.ilike(f'%{search}%') |
            Trek.location.ilike(f'%{search}%')
        )
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if location:
        query = query.filter(Trek.location.ilike(f'%{location}%'))
    if max_price and str(max_price).replace('.', '').isdigit():
        query = query.filter(Trek.price <= float(max_price))

    treks = query.order_by(Trek.start_date).all()
    result = [t.to_dict() for t in treks]

    # Cache only unfiltered results
    if not search and not difficulty and not location and not max_price:
        redis_client.setex('open_treks', 300, json.dumps(result))

    return jsonify(result), 200


@user_bp.route('/treks/<int:trek_id>', methods=['GET'])
@jwt_required()
@user_required
def get_trek(trek_id):
    # Try cache
    cached = redis_client.get(f'trek_{trek_id}')
    if cached:
        return jsonify(json.loads(cached)), 200

    trek = Trek.query.get_or_404(trek_id)
    result = trek.to_dict()

    redis_client.setex(f'trek_{trek_id}', 300, json.dumps(result))
    return jsonify(result), 200



@user_bp.route('/bookings', methods=['GET'])
@jwt_required()
@user_required
def get_bookings():
    user_id = int(get_jwt_identity())
    status = request.args.get('status', '')
    query = Booking.query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status)

    bookings = query.order_by(Booking.booking_date.desc()).all()
    return jsonify([b.to_dict() for b in bookings]), 200


@user_bp.route('/bookings', methods=['POST'])
@jwt_required()
@user_required
def book_trek():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    trek_id = data.get('trek_id')
    if not trek_id:
        return jsonify({'error': 'Trek ID required'}), 400

    trek = Trek.query.get_or_404(trek_id)
    num_participants = int(data.get('num_participants', 1))
    special_requirements = data.get('special_requirements', '')

    if trek.status != 'Open':
        return jsonify({'error': 'Trek is not open for booking'}), 400
    existing = Booking.query.filter_by(
        user_id=user_id,
        trek_id=trek_id,
        status='Booked'
    ).first()
    if existing:
        return jsonify({'error': 'You have already booked this trek'}), 400
    if trek.available_slots < num_participants:
        return jsonify({
            'error': f'Only {trek.available_slots} slots available'
        }), 400

    booking = Booking(
        user_id=user_id,
        trek_id=trek_id,
        num_participants=num_participants,
        special_requirements=special_requirements,
        status='Booked'
    )
    trek.available_slots -= num_participants
    db.session.add(booking)
    db.session.commit()

    # Invalidate trek cache
    redis_client.delete(f'trek_{trek_id}')
    redis_client.delete('open_treks')

    return jsonify({
        'message': f'Successfully booked {trek.name}!',
        'booking': booking.to_dict()
    }), 201


@user_bp.route('/bookings/<int:booking_id>/cancel', methods=['PUT'])
@jwt_required()
@user_required
def cancel_booking(booking_id):
    user_id = int(get_jwt_identity())
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != user_id:
        return jsonify({'error': 'Not authorized'}), 403

    if booking.status != 'Booked':
        return jsonify({'error': 'Booking cannot be cancelled'}), 400

    booking.status = 'Cancelled'
    booking.trek.available_slots += booking.num_participants
    booking.updated_at = datetime.utcnow()
    db.session.commit()

    # Invalidate cache
    redis_client.delete(f'trek_{booking.trek_id}')
    redis_client.delete('open_treks')

    return jsonify({'message': 'Booking cancelled successfully'}), 200


@user_bp.route('/history', methods=['GET'])
@jwt_required()
@user_required
def get_history():
    user_id = int(get_jwt_identity())
    completed = Booking.query.filter_by(
        user_id=user_id,
        status='Completed'
    ).all()
    cancelled = Booking.query.filter_by(
        user_id=user_id,
        status='Cancelled'
    ).all()
    return jsonify({
        'completed': [b.to_dict() for b in completed],
        'cancelled': [b.to_dict() for b in cancelled]
    }), 200

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
@user_required
def get_profile():
    user = User.query.get(int(get_jwt_identity()))
    return jsonify(user.to_dict()), 200


@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
@user_required
def update_profile():
    user = User.query.get(int(get_jwt_identity()))
    data = request.get_json()

    user.name = data.get('name', user.name)
    user.phone = data.get('phone', user.phone)
    user.emergency_contact = data.get(
        'emergency_contact', user.emergency_contact)
    user.emergency_phone = data.get('emergency_phone', user.emergency_phone)

    age = data.get('age')
    if age:
        user.age = int(age)

    new_password = data.get('new_password')
    if new_password:
        if len(new_password) < 6:
            return jsonify({
                'error': 'Password must be at least 6 characters'
            }), 400
        confirm = data.get('confirm_password')
        if new_password != confirm:
            return jsonify({'error': 'Passwords do not match'}), 400
        user.set_password(new_password)

    db.session.commit()
    return jsonify({
        'message': 'Profile updated!',
        'user': user.to_dict()
    }), 200


@user_bp.route('/export', methods=['POST'])
@jwt_required()
@user_required
def export_bookings():
    user_id = int(get_jwt_identity())

    from celery_worker import export_booking_csv
    task = export_booking_csv.delay(user_id)

    return jsonify({
        'message': 'Export started. You will be notified when ready.',
        'task_id': task.id
    }), 202


@user_bp.route('/export/<task_id>', methods=['GET'])
@jwt_required()
@user_required
def get_export_status(task_id):
    from celery_worker import export_booking_csv
    task = export_booking_csv.AsyncResult(task_id)

    if task.state == 'PENDING':
        return jsonify({'status': 'pending'}), 200
    elif task.state == 'SUCCESS':
        return jsonify({
            'status': 'completed',
            'data': task.result
        }), 200
    else:
        return jsonify({'status': task.state}), 200
