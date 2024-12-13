from .base import Base, env


class Dev(Base):
    DEBUG = True
    ALLOWED_HOSTS = ["*"]

    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True

    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    SENTRY_DSN = env("SENTRY_DSN", default=None)
