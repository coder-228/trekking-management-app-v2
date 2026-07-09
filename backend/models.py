from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), nullable=False, default='user')
    # role can be: 'admin', 'staff', 'user'
    status = db.Column(db.String(20), default='active')
    # status can be: 'active', 'blacklisted', 'pending'
    experience_years = db.Column(db.Integer, default=0)
    specialization = db.Column(db.String(200))
    age = db.Column(db.Integer)
    emergency_contact = db.Column(db.String(120))
    emergency_phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy=True)
    treks = db.relationship('Trek', backref='assigned_staff', lazy=True,
                            foreign_keys='Trek.staff_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'role': self.role,
            'status': self.status,
            'experience_years': self.experience_years,
            'specialization': self.specialization,
            'age': self.age,
            'created_at': self.created_at.strftime('%d %b %Y')
        }


class Trek(db.Model):
    __tablename__ = 'treks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    difficulty = db.Column(db.String(20), nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    total_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, default=0.0)
    altitude = db.Column(db.String(50))
    status = db.Column(db.String(20), default='Pending')
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    bookings = db.relationship('Booking', backref='trek', lazy=True)

    @property
    def booked_slots(self):
        return Booking.query.filter_by(
            trek_id=self.id, status='Booked').count()

    @property
    def completion_percent(self):
        if self.total_slots == 0:
            return 0
        return int((self.booked_slots / self.total_slots) * 100)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'description': self.description,
            'difficulty': self.difficulty,
            'duration_days': self.duration_days,
            'total_slots': self.total_slots,
            'available_slots': self.available_slots,
            'booked_slots': self.booked_slots,
            'completion_percent': self.completion_percent,
            'price': self.price,
            'altitude': self.altitude,
            'status': self.status,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'staff_id': self.staff_id,
            'staff_name': self.assigned_staff.name if self.assigned_staff else None,
            'created_at': self.created_at.strftime('%d %b %Y')
        }


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Booked')
    num_participants = db.Column(db.Integer, default=1)
    special_requirements = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.name,
            'trek_id': self.trek_id,
            'trek_name': self.trek.name,
            'trek_location': self.trek.location,
            'trek_difficulty': self.trek.difficulty,
            'booking_date': self.booking_date.strftime('%d %b %Y'),
            'status': self.status,
            'num_participants': self.num_participants,
            'special_requirements': self.special_requirements,
            'start_date': self.trek.start_date.strftime('%d %b %Y') if self.trek.start_date else None
        }
