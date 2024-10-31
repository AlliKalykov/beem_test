import os

from configurations.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "abc_back.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "DEV")


application = get_asgi_application()
