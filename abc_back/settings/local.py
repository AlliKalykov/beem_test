from .base import Base, env


class Local(Base):
    DEBUG = env("DEBUG", default=True)
    ALLOWED_HOSTS = ["*"]

    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_CREDENTIALS = True
