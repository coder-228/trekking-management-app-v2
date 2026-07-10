from flask import Flask
from config import Config
from extensions import db, jwt, cors
from werkzeug.security import generate_password_hash


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={
        r"/api/*": {"origins": "http://localhost:5173"}
    })

    # Register blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.staff import staff_bp
    from routes.user import user_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(staff_bp, url_prefix='/api/staff')
    app.register_blueprint(user_bp, url_prefix='/api/user')

    with app.app_context():
        db.create_all()
        seed_data()

    return app


def seed_data():
    from models import User, Trek
    from datetime import date

    # Seed admin
    if not User.query.filter_by(role='admin').first():
        admin = User(
            username='admin',
            email='admin@trek.com',
            name='Super Admin',
            role='admin',
            status='active'
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # Seed sample staff
        staff1 = User(
            username='ravi',
            email='ravi@trek.com',
            name='Ravi Kumar',
            role='staff',
            status='active',
            phone='+91-9876543210',
            experience_years=8,
            specialization='High-altitude trekking'
        )
        staff1.set_password('ravi123')
        db.session.add(staff1)

        # Seed sample user
        user1 = User(
            username='john',
            email='john@trek.com',
            name='John Doe',
            role='user',
            status='active',
            phone='+91-9000000001',
            age=28
        )
        user1.set_password('john123')
        db.session.add(user1)
        db.session.flush()

        # Seed sample treks
        treks = [
            Trek(name='Kedarnath Trek', location='Uttarakhand',
                 difficulty='Hard', duration_days=6,
                 total_slots=20, available_slots=20,
                 price=8500, altitude='3583m', status='Open',
                 staff_id=staff1.id,
                 start_date=date(2024, 5, 15),
                 end_date=date(2024, 5, 21),
                 description='Sacred journey through Himalayan scenery.'),
            Trek(name='Triund Trek', location='Himachal Pradesh',
                 difficulty='Easy', duration_days=2,
                 total_slots=40, available_slots=40,
                 price=2000, altitude='2875m', status='Open',
                 start_date=date(2024, 4, 20),
                 end_date=date(2024, 4, 22),
                 description='Beginner friendly with stunning views.'),
            Trek(name='Valley of Flowers', location='Uttarakhand',
                 difficulty='Moderate', duration_days=4,
                 total_slots=30, available_slots=30,
                 price=5500, altitude='3658m', status='Approved',
                 staff_id=staff1.id,
                 start_date=date(2024, 6, 10),
                 end_date=date(2024, 6, 14),
                 description='UNESCO World Heritage alpine flowers.'),
        ]
        db.session.add_all(treks)
        db.session.commit()
        print('Database seeded!')


app = create_app()

from celery_worker import init_celery
celery = init_celery(app)

if __name__ == '__main__':
    app.run(debug=True)
