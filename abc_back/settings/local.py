from .base import Base, env


class Local(Base):
    DEBUG = env("DEBUG", default=True)
    ALLOWED_HOSTS = ["*"]

    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_CREDENTIALS = True

    SENTRY_DSN = env("SENTRY_DSN", default=None)
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
