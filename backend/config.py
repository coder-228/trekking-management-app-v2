import os
from datetime import timedelta

class Config:
    # Flask
    SECRET_KEY = 'trekking-v2'
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///trekking_v2.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = 'jwt'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Redis
    REDIS_URL = 'redis://localhost:6379/0'
    
    # Celery
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    
    # Mail (for celery jobs)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'email@gmail.com'
    MAIL_PASSWORD = 'password'
