"""
Django settings for project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'reversion',
    'dnsmanager',
    'rest_framework',

    'project.account',
    'project.couch',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_PATH, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'project.context_processor.app_name',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'www', 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'www', 'media')
MEDIA_URL = '/media/'

# Settings from .env (optional load)
from dj_database_url import config as db_config
DATABASES = {'default': db_config(default='sqlite://localhost//%s' % os.path.join(BASE_DIR, 'db', 'project.sqlite3'))}
TIME_ZONE = os.environ.setdefault('TIME_ZONE', "Australia/Sydney")
EMAIL_HOST = os.environ.setdefault('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.environ.setdefault('EMAIL_PORT', '25'))
SERVER_EMAIL = os.environ.get('SERVER_EMAIL')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

ADMINS = ()
for admin in os.environ.get('ADMINS', '').split():
    ADMINS = ADMINS + (tuple(admin.split('/')),)
MANAGERS = ADMINS

DEBUG = bool(os.environ.get('DEBUG', 'False').lower() in ("true", "yes", "t", "1"))
TEMPLATE_DEBUG = DEBUG
if os.environ.get('DEBUG_EMAIL', False):
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Loading SECRET_KEY from .env variable
try:
    SECRET_KEY = os.environ['SECRET_KEY']
except KeyError:
    print("Warning: settings.SECRET_KEY is not set!")
    pass

from dnsmanager.defaults import DNS_MANAGER_RECIPES_DEFAULT
DNS_MANAGER_RECIPES = DNS_MANAGER_RECIPES_DEFAULT + (
    ('project.dns_manager_recipes.VoltGridEmail', 'Set Volt Grid MX'),
    ('project.dns_manager_recipes.VoltGridNameServers', 'Set Volt Grid NS'),
    ('project.dns_manager_recipes.CromovaNameServers', 'Set CroMoVa NS'),
    ('project.dns_manager_recipes.PanuboNameServers', 'Set Panubo NS'),
)
DNS_MANAGER_DOMAIN_MODEL = 'project.account.Domain'
DNS_MANAGER_ZONE_ADMIN_FILTER = ('domain__organisation', )
DNS_MANAGER_NAMESERVERS = os.environ.get('DNS_MANAGER_NAMESERVERS', None)

# CouchDB Config
COUCH_DATABASES = {
    'dns': {
        'NAME': os.environ.setdefault('COUCHDB_DNS_NAME', 'dns'),
        'USER': os.environ.setdefault('COUCHDB_DNS_USER', 'admin'),
        'PASS': os.environ.setdefault('COUCHDB_DNS_PASS', 'admin'),
        'HOST': os.environ.setdefault('COUCHDB_DNS_HOST', 'http://127.0.0.1:5984'),
    }
}
COUCH_IGNORE_MISSING = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'PAGINATE_BY': 100
}

# Redis cache for DNS MANAGER
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "%s/1" % REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Custom attributes
APP_NAME = 'Panubo DNS'

# Django Sites
SITE_ID = 1