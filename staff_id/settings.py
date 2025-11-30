from pathlib import Path
from decouple import config
import os

BASE_DIR = Path(__file__).resolve().parent.parent


CSRF_TRUSTED_ORIGINS = ['https://*.railway.app']

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')

INSTALLED_APPS = [
    'staff.apps.StaffConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_htmx'
]

SITE_DOMAIN = config('SITE_DOMAIN', default='localhost:8000')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'staff_id.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'staff.context_processors.hospital_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'staff_id.wsgi.application'



STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('PGDATABASE'),
#         'USER': config('PGUSER'),
#         'PASSWORD': config('PGPASSWORD'),
#         'HOST': config('PGHOST'),
#         'PORT': config('PGPORT', default='5432'),
#         'CONN_MAX_AGE': 600,
#         'OPTIONS': {
#             'connect_timeout': 10,
#             'server_side_binding': True,
#         },
#         'CONN_HEALTH_CHECKS': True,
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('PGDATABASE', default=os.environ.get('PGDATABASE', '')),
        'USER': config('PGUSER', default=os.environ.get('PGUSER', '')),
        'PASSWORD': config('PGPASSWORD', default=os.environ.get('PGPASSWORD', '')),
        'HOST': config('PGHOST', default=os.environ.get('PGHOST', '')),
        'PORT': config('PGPORT', default=os.environ.get('PGPORT', '5432')),
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'connect_timeout': 10,
            'server_side_binding': True,
        },
        'CONN_HEALTH_CHECKS': True,
    }
}

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


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True
DATE_INPUT_FORMATS = ['%d-%m-%Y'] 
DATETIME_INPUT_FORMATS = ['%d-%m-%Y %H:%M:%S', '%d-%m-%Y']

LOGIN_REDIRECT_URL = '/'
LOGIN_URL="/login/"
LOGOUT_REDIRECT_URL = '/'

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom settings
HOSPITAL_NAME = config('HOSPITAL_NAME', default='National Orthopaedic Hospital, Dala')
