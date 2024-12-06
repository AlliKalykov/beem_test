from .base import Base


class Dev(Base):
    DEBUG = True
    ALLOWED_HOSTS = ["*"]
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:300",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://31.129.97.238:8000",
    ]

    CORS_ALLOW_CREDENTIALS = True

    CORS_ALLOW_ORIGINS = [
        "http://localhost:300",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://31.129.97.238:8000",
    ]

    CORS_ALLOW_HEADERS = "*"

    CORS_ORIGIN_WHITELIST = [
        "http://localhost:300",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://31.129.97.238:8000",
    ]
