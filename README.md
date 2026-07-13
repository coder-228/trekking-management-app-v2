# SummitQuest — Trekking Management App V2

A trekking management web app built with Vue.js and Flask.
Three roles: Admin, Trek Staff, and Trekker.

---

## Prerequisites
- Python 3.x
- Node.js — https://nodejs.org/en
- Redis for Windows — install Redis-x64-3.0.504.msi from
  https://github.com/microsoftarchive/redis/releases

---

## How To Run

You need 4 terminal windows open simultaneously.

### Window 1 — Backend
cd backend
pip install flask flask-sqlalchemy flask-jwt-extended flask-cors celery redis==4.6.0
python app.py
Runs on http://localhost:5000

### Window 2 — Frontend
cd frontend
npm install
npm run dev
Runs on http://localhost:5173 — open this in browser

### Window 3 — Celery Worker
cd backend
python -m celery -A celery_worker.celery beat --loglevel=info

---

## Login Credentials (Data seeded programmically)

| Role  | Username | Password |
|-------|----------|----------|
| Admin | admin    | admin123 |
| Staff | ravi     | ravi123  |
| User  | john     | john123  |

---

## Notes
- Database created automatically on first run
- Redis must be running before starting backend
- Verify Redis with: redis-cli ping → should return PONG

