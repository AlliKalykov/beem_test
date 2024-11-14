from .base import Base


class CI(Base):
    PROJECT_ENVIRONMENT = "CI"

    DEBUG = True
    ALLOWED_HOSTS = ["*"]

    SENTRY_DSN = None

    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    # SMTP
    EMAIL_HOST = "xxx"
    EMAIL_PORT = "xxx"
    EMAIL_HOST_USER = "xxx"
    EMAIL_HOST_PASSWORD = "xxx"

    SECRET_KEY = "xxx"
