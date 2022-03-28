import os
from core.settings.base import *

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['185.235.41.234', 'scarfly.ir', 'api.scarfly.ir']

STATIC_ROOT = '/vol/web/static'
MEDIA_ROOT = '/vol/web/media'
MEDIA_URL = '/media/'

INSTALLED_APPS += ['corsheaders']
MIDDLEWARE += ['corsheaders.middleware.CorsMiddleware', ]
CORS_ORIGIN_ALLOW_ALL = True  # ToDo

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': "5432",
    }
}

TELEGRAM = {
    'bot_token': os.getenv('TELEGRAM_BOT_BOT_TOKEN'),
    'channel_username': '@scarfly_ir',
    'full_url': 'https://api.scarfly.ir',
}

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
ZP_MERCHANT = os.getenv('ZP_MERCHANT')
