from .base import Base


class Dev(Base):
    DEBUG = True
    ALLOWED_HOSTS = ["*"]

    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_CREDENTIALS = True
