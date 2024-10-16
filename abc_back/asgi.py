import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abc_back.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'DEV')

from configurations.asgi import get_asgi_application


application = get_asgi_application()
