import os
from core.settings.base import *

DEBUG = bool(int(os.getenv("DEBUG")))
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['0.0.0.0', 'scarfly.ir', 'api.scarfly.ir', 'www.scarfly.ir', 'www.api.scarfly.ir']

STATIC_ROOT = BASE_DIR / 'static'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_URL = '/api/static/'
MEDIA_URL = '/api/media/'

INSTALLED_APPS += ['corsheaders', 'admin_honeypot']
MIDDLEWARE += ['corsheaders.middleware.CorsMiddleware', ]
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'https://scarfly.ir',
)

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
    'full_url': 'https://scarfly.ir',
}

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
ZP_MERCHANT = os.getenv('ZP_MERCHANT')
