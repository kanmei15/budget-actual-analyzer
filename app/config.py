from datetime import timedelta
import os

class Config:
    DEBUG = False
    POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "mydb")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")


    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')

    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'fallback-jwt-secret-key')
    JWT_TOKEN_LOCATION = os.environ.get('JWT_TOKEN_LOCATION', 'cookies')

    CONTENT_SECURITY_POLICY = {
        'default-src': ["'self'"],
        'script-src': ["'self'"],
        'style-src': ["'self'", 'https://fonts.googleapis.com'],
        'font-src': ["'self'", 'https://fonts.gstatic.com', 'data:'],
    }

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # アップロードファイル5MB制限

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    SESSION_COOKIE_SECURE = False
    JWT_COOKIE_SAMESITE = 'Strict'
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = True

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SAMESITE = 'Strict'
    SESSION_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = 'Strict'
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True

class TestingConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False
    JWT_COOKIE_SAMESITE = 'Lax'
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False