from celery import Celery, Task
from celery.schedules import crontab
import csv
import io
import os
from datetime import datetime, date

celery = Celery(
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)


def init_celery(app):
    celery.conf.update(
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )

    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = FlaskTask

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


@celery.task(name='celery_worker.send_daily_reminders')
def send_daily_reminders():
    from app import app
    with app.app_context():
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


@celery.task(name='celery_worker.send_monthly_report')
def send_monthly_report():
    from app import app
    with app.app_context():
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
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Monthly Report — {month}</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background: #f8fffe;
                    color: #0d1f17;
                    padding: 2rem;
                }}
                .header {{
                    background: linear-gradient(135deg, #1a3d2b, #2d6a4f);
                    color: white;
                    padding: 2.5rem;
                    border-radius: 16px;
                    margin-bottom: 2rem;
                    position: relative;
                    overflow: hidden;
                }}
                .header::after {{
                    content: '▲';
                    position: absolute;
                    right: 2rem;
                    top: 50%;
                    transform: translateY(-50%);
                    font-size: 6rem;
                    opacity: 0.08;
                }}
                .header h1 {{
                    font-size: 1.8rem;
                    font-weight: 900;
                    margin-bottom: 0.25rem;
                }}
                .header p {{
                    opacity: 0.75;
                    font-size: 0.9rem;
                }}
                .badge {{
                    display: inline-block;
                    background: rgba(82,183,136,0.3);
                    color: #b7e4c7;
                    padding: 0.25rem 0.75rem;
                    border-radius: 20px;
                    font-size: 0.78rem;
                    margin-top: 0.5rem;
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 1rem;
                    margin-bottom: 2rem;
                }}
                .stat-card {{
                    border-radius: 12px;
                    padding: 1.5rem;
                    color: white;
                    text-align: center;
                }}
                .stat-card.green {{ background: linear-gradient(135deg, #1a3d2b, #2d6a4f); }}
                .stat-card.sage {{ background: linear-gradient(135deg, #52b788, #40916c); }}
                .stat-card.orange {{ background: linear-gradient(135deg, #f4a261, #e0801a); }}
                .stat-card.red {{ background: linear-gradient(135deg, #e76f51, #c1440e); }}
                .stat-num {{
                    font-size: 2.5rem;
                    font-weight: 900;
                    line-height: 1;
                }}
                .stat-label {{
                    font-size: 0.82rem;
                    opacity: 0.85;
                    margin-top: 0.25rem;
                }}
                .section {{
                    background: white;
                    border-radius: 16px;
                    box-shadow: 0 4px 24px rgba(26,61,43,0.1);
                    margin-bottom: 1.5rem;
                    overflow: hidden;
                }}
                .section-header {{
                    padding: 1rem 1.5rem;
                    border-bottom: 1px solid rgba(26,61,43,0.08);
                    font-weight: 700;
                    color: #1a3d2b;
                    font-size: 1rem;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th {{
                    background: #f8fffe;
                    font-size: 0.78rem;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    color: #6c757d;
                    padding: 0.75rem 1.5rem;
                    text-align: left;
                    font-weight: 600;
                    border-bottom: 2px solid rgba(26,61,43,0.08);
                }}
                td {{
                    padding: 0.85rem 1.5rem;
                    border-bottom: 1px solid rgba(26,61,43,0.05);
                    font-size: 0.88rem;
                }}
                tr:last-child td {{ border-bottom: none; }}
                tr:hover td {{ background: rgba(82,183,136,0.04); }}
                .rank {{
                    font-weight: 700;
                    color: #1a3d2b;
                }}
                .badge-easy {{ background: #d8f3dc; color: #1b4332; padding: 2px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }}
                .badge-moderate {{ background: #fff3cd; color: #664d03; padding: 2px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }}
                .badge-hard {{ background: #f8d7da; color: #58151c; padding: 2px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }}
                .badge-open {{ background: #d8f3dc; color: #1b4332; padding: 2px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }}
                .badge-closed {{ background: #f8d7da; color: #58151c; padding: 2px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }}
                .badge-completed {{ background: #e2d9f3; color: #4a235a; padding: 2px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }}
                .footer {{
                    text-align: center;
                    padding: 1.5rem;
                    color: #6c757d;
                    font-size: 0.82rem;
                    border-top: 1px solid rgba(26,61,43,0.08);
                    margin-top: 2rem;
                }}
                .progress-bar {{
                    height: 6px;
                    background: rgba(26,61,43,0.1);
                    border-radius: 3px;
                    overflow: hidden;
                    width: 100px;
                }}
                .progress-fill {{
                    height: 100%;
                    background: #52b788;
                    border-radius: 3px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="badge">▲ TMA</div>
                <h1 style="margin-top:0.75rem;">Monthly Activity Report</h1>
                <p>{month}</p>
                <p style="margin-top:0.25rem;">Generated on {today.strftime('%d %B %Y')}</p>
            </div>
            <div class="stats-grid">
                <div class="stat-card green">
                    <div class="stat-num">{total_treks}</div>
                    <div class="stat-label">Total Treks</div>
                </div>
                <div class="stat-card sage">
                    <div class="stat-num">{total_users}</div>
                    <div class="stat-label">Total Trekkers</div>
                </div>
                <div class="stat-card orange">
                    <div class="stat-num">{total_bookings}</div>
                    <div class="stat-label">Total Bookings</div>
                </div>
                <div class="stat-card red">
                    <div class="stat-num">{active_bookings}</div>
                    <div class="stat-label">Active Bookings</div>
                </div>
            </div>
            <div class="section">
                <div class="section-header">🏆 Top Popular Treks</div>
                <table>
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Trek Name</th>
                            <th>Location</th>
                            <th>Difficulty</th>
                            <th>Bookings</th>
                            <th>Status</th>
                            <th>Occupancy</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(f"""
                        <tr>
                            <td class="rank">#{i+1}</td>
                            <td><strong>{t.name}</strong></td>
                            <td>{t.location}</td>
                            <td><span class="badge-{t.difficulty.lower()}">{t.difficulty}</span></td>
                            <td><strong>{t.booked_slots}</strong></td>
                            <td><span class="badge-{t.status.lower()}">{t.status}</span></td>
                            <td>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width:{t.completion_percent}%"></div>
                                </div>
                                <small style="color:#6c757d;font-size:0.75rem;">{t.completion_percent}%</small>
                            </td>
                        </tr>
                        """ for i, t in enumerate(popular))}
                    </tbody>
                </table>
            </div>
            <div class="footer">
                ▲ Trekking Management System &nbsp;·&nbsp;
                Confidential — For Admin Use Only &nbsp;·&nbsp; 
                {today.strftime('%d %B %Y')}
            </div>
        </body>
        </html>
        """
        report_filename = f'report_{today.strftime("%Y_%m")}.html'
        report_path = os.path.join(os.path.dirname(__file__), 'reports', report_filename)
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_html)
        print(f'MONTHLY REPORT SAVED → {report_path}')
        return {
            'month': month,
            'total_treks': total_treks,
            'total_bookings': total_bookings,
            'report_path': report_path,
            'report_generated': str(today)
        }

@celery.task(name='celery_worker.export_booking_csv')
def export_booking_csv(user_id):
    from app import app
    with app.app_context():
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
