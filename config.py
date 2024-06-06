from datetime import timedelta


class Config:
    SECRET_KEY = 'super-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///example.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'some_salt'
    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    JWT_SECRET_KEY = 'your_jwt_secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
    CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
    CELERY_CACHE_BACKEND = "redis://127.0.0.1:6379/0"
    BROKER_URL = "redis://127.0.0.1:6379/0"
    RESULT_BACKEND = "redis://127.0.0.1:6379/0"
    CACHE_BACKEND = "redis://127.0.0.1:6379/0"
