import datetime
import logging
import sentry_sdk
import socket

from pathlib import Path

from configurations import Configuration, values

from django.utils.functional import cached_property

from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration


from abc_back.logging import LoggerDescriptor

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class Common(Configuration):
    log = LoggerDescriptor(__name__)

    PROJECT_NAME = "ABC Concierge"
    PROJECT_BASE_URL = values.Value("http://localhost:9000")

    PROJECT_ENVIRONMENT = values.Value("development")

    SECRET_KEY = "django-insecure-1"

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = []


    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'django_extensions',

        "rest_framework",
        "drf_spectacular",

        "corsheaders",

        "django_celery_beat",

        "debug_toolbar",

        'abc_back.users.apps.UsersConfig',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',

        "corsheaders.middleware.CorsMiddleware",

        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',

        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    ROOT_URLCONF = 'abc_back.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates']
            ,
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'abc_back.wsgi.application'

    SHELL_PLUS = "ipython"
    SHELL_PLUS_PRINT_SQL = True
    # Truncate sql queries to this number of characters (this is the default)
    SHELL_PLUS_PRINT_SQL_TRUNCATE = 1000
    # To disable truncation of sql queries use
    SHELL_PLUS_PRINT_SQL_TRUNCATE = None

    # Database
    # https://docs.djangoproject.com/en/5.1/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }

        # 'default': {
        #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #     'NAME': 'abc_concierge',
        #     'USER': 'postgres',
        #     'PASSWORD': 'postgres',
        #     'HOST': 'localhost',
        #     'PORT': '5432',
        # }
    }


    # Password validation
    # https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    # AUTHENTICATION
    LOGIN_URL = "/"
    LOGIN_REDIRECT_URL = "/"
    USER_FIELDS = ["email"]
    AUTH_USER_MODEL = "users.User"
    AUTHENTICATION_BACKENDS = [
        "django.contrib.auth.backends.ModelBackend",
    ]

    # REST_FRAMEWORK
    DEFAULT_PAGE_SIZE = 10
    REST_FRAMEWORK = {
        "DEFAULT_PARSER_CLASSES": [
            "rest_framework.parsers.JSONParser", "rest_framework.parsers.FormParser",
            "rest_framework.parsers.MultiPartParser",
        ],
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework_simplejwt.authentication.JWTAuthentication",
        ],
        "DEFAULT_PERMISSION_CLASSES": [
            "rest_framework.permissions.IsAuthenticated",
        ],
        "DEFAULT_FILTER_BACKENDS": [
            "django_filters.rest_framework.DjangoFilterBackend",
        ],
        "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
        "EXCEPTION_HANDLER": "abc_back.sentry_exception_handler.sentry_exception_handler",
        "REST_FRAMEWORK_TOKEN_EXPIRE_DAYS": 7,  # TODO: добавить в .env?
    }

    # Simple JWT
    SIMPLE_JWT = {
        "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=5),
        "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=1),
        "ROTATE_REFRESH_TOKENS": False,
        "BLACKLIST_AFTER_ROTATION": False,
        "UPDATE_LAST_LOGIN": False,

        "ALGORITHM": "HS256",
        "SIGNING_KEY": SECRET_KEY,
        "VERIFYING_KEY": None,
        "AUDIENCE": None,
        "ISSUER": None,
        "JWK_URL": None,
        "LEEWAY": 0,

        "AUTH_HEADER_TYPES": "Bearer",
        "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
        "USER_ID_FIELD": "id",
        "USER_ID_CLAIM": "user_id",
        "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

        "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
        "TOKEN_TYPE_CLAIM": "token_type",
        "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

        "JTI_CLAIM": "jti",

        "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
        "SLIDING_TOKEN_LIFETIME": datetime.timedelta(minutes=5),
        "SLIDING_TOKEN_REFRESH_LIFETIME": datetime.timedelta(days=1),
    }

    @cached_property
    def SPECTACULAR_SETTINGS(self):
        return {
            "TITLE": f"{self.PROJECT_NAME} API",
            "VERSION": None,
            "SCHEMA_PATH_PREFIX": r"/api/v[0-9]+/",
            "SCHEMA_PATH_PREFIX_TRIM": True,
            "SERVE_AUTHENTICATION": ["rest_framework.authentication.SessionAuthentication"],
            "SERVE_PERMISSIONS": ["abc_back.api.permissions.IsSuperUser"],
            "SERVERS": [{"url": f"{self.PROJECT_BASE_URL}/api/v1"}],
            "COMPONENT_SPLIT_REQUEST": True,
        }

    # Internationalization
    # https://docs.djangoproject.com/en/5.1/topics/i18n/

    # Internationalization
    LANGUAGE_CODE = "ru-ru"
    TIME_ZONE = "Europe/Moscow"
    USE_I18N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/5.1/howto/static-files/

    # Static
    STATIC_URL = values.Value("static/")
    STATIC_ROOT = BASE_DIR / "static"

    # Media
    MEDIA_URL = values.Value("media/")
    MEDIA_ROOT = BASE_DIR / "media"

    # Default primary key field type
    # https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    @cached_property
    def CELERY(self):
        celery_config = {
            "broker_url": values.Value("memory://", name="REDIS_BROKER_URL"),
            "timezone": self.TIME_ZONE,
            "task_default_queue": f"{self.PROJECT_NAME.lower()}_default",
            "task_soft_time_limit": values.IntegerValue(3600, name="CELERY_TASK_SOFT_TIME_LIMIT"),
            "task_time_limit": values.IntegerValue(7200, name="CELERY_TASK_HARD_TIME_LIMIT"),
        }
        if result_backend := values.URLValue(None, name="REDIS_CACHE_URL"):
            celery_config["result_backend"] = result_backend
            celery_config["result_extended"] = True
        return celery_config

    # Sentry settings
    SENTRY_DSN = values.URLValue(None)
    SENTRY_TRACES_SAMPLE_RATE = values.FloatValue(0.0)

    @classmethod
    def post_setup(cls):
        super().post_setup()
        logging.basicConfig(level=logging.INFO, format="*** %(message)s")
        cls.log.info(f"Starting {cls.PROJECT_NAME} project using {cls.__name__} configuration")

        if cls.SENTRY_DSN:
            cls.log.info(f"Sentry is enabled, environment: {cls.PROJECT_ENVIRONMENT}")
            sentry_sdk.init(
                dsn=cls.SENTRY_DSN,
                environment=cls.PROJECT_ENVIRONMENT,
                integrations=[
                    DjangoIntegration(),
                    RedisIntegration(),
                ],
                traces_sample_rate=cls.SENTRY_TRACES_SAMPLE_RATE,
                send_default_pii=True,
            )
        else:
            cls.log.info("Sentry is disabled")

    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_HEADERS = "*"
    CORS_ALLOWED_ORIGINS = [
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    CORS_ORIGIN_WHITELIST = [
    ]

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]


class Dev(Common):
    DEBUG = True
    ALLOWED_HOSTS = ['*']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_CREDENTIALS = True
