from celery import Celery
from celery.schedules import crontab
import csv
import io
from datetime import datetime, date

celery = Celery(
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)


def make_celery(app):
    celery.conf.update(
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def init_celery(app):
    make_celery(app)

    celery.conf.beat_schedule = {
        'daily-trek-reminder': {
            'task': 'celery_worker.send_daily_reminders',
            'schedule': crontab(hour=8, minute=0),
        },
        'monthly-admin-report': {
            'task': 'celery_worker.send_monthly_report',
            'schedule': crontab(day_of_month=1, hour=9, minute=0),
        },
    }

    return celery


# ---- JOB 1 — DAILY REMINDERS ----

@celery.task(name='celery_worker.send_daily_reminders')
def send_daily_reminders():
    from models import Booking
    today = date.today()
    upcoming_bookings = Booking.query.filter_by(status='Booked').all()

    reminders_sent = 0
    for booking in upcoming_bookings:
        if booking.trek.start_date:
            days_until = (booking.trek.start_date - today).days
            if 0 <= days_until <= 3:
                print(f'REMINDER: {booking.user.name} — '
                      f'{booking.trek.name} starts in {days_until} days')
                reminders_sent += 1

    return {'reminders_sent': reminders_sent, 'date': str(today)}


# ---- JOB 2 — MONTHLY REPORT ----

@celery.task(name='celery_worker.send_monthly_report')
def send_monthly_report():
    from models import Trek, Booking, User
    today = date.today()
    month = today.strftime('%B %Y')

    total_treks = Trek.query.count()
    total_bookings = Booking.query.count()
    total_users = User.query.filter_by(role='user').count()
    active_bookings = Booking.query.filter_by(status='Booked').count()

    all_treks = Trek.query.all()
    popular = sorted(
        all_treks, key=lambda t: t.booked_slots, reverse=True)[:5]

    report_html = f"""
    <html>
    <body style="font-family: Arial; padding: 20px;">
        <h1>SummitQuest Monthly Report — {month}</h1>
        <hr>
        <h2>Summary</h2>
        <ul>
            <li>Total Treks: {total_treks}</li>
            <li>Total Users: {total_users}</li>
            <li>Total Bookings: {total_bookings}</li>
            <li>Active Bookings: {active_bookings}</li>
        </ul>
        <h2>Popular Treks</h2>
        <table border="1" cellpadding="8">
            <tr>
                <th>Trek</th>
                <th>Location</th>
                <th>Bookings</th>
                <th>Status</th>
            </tr>
            {''.join(f"""
            <tr>
                <td>{t.name}</td>
                <td>{t.location}</td>
                <td>{t.booked_slots}</td>
                <td>{t.status}</td>
            </tr>
            """ for t in popular)}
        </table>
        <hr>
        <p>Generated on {today.strftime('%d %b %Y')}</p>
    </body>
    </html>
    """

    print(f'MONTHLY REPORT GENERATED for {month}')
    return {
        'month': month,
        'total_treks': total_treks,
        'total_bookings': total_bookings,
        'report_generated': str(today)
    }


# ---- JOB 3 — EXPORT CSV ----

@celery.task(name='celery_worker.export_booking_csv')
def export_booking_csv(user_id):
    from models import Booking
    bookings = Booking.query.filter_by(user_id=user_id).all()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        'Booking ID', 'Trek Name', 'Location',
        'Difficulty', 'Start Date', 'Booking Date',
        'Participants', 'Status'
    ])

    for b in bookings:
        writer.writerow([
            b.id,
            b.trek.name,
            b.trek.location,
            b.trek.difficulty,
            b.trek.start_date.strftime('%d %b %Y') if b.trek.start_date else 'TBD',
            b.booking_date.strftime('%d %b %Y'),
            b.num_participants,
            b.status
        ])

    csv_content = output.getvalue()
    print(f'CSV EXPORT for user {user_id} done')

    return {
        'user_id': user_id,
        'csv_data': csv_content,
        'total_rows': len(bookings),
        'generated_at': str(datetime.utcnow())
    }
