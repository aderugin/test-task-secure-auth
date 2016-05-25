# -*- coding: utf-8 -*-
"""
    Project settings
"""
import os


# ==============================================================================
# Django
# ==============================================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_DIR = os.path.dirname(BASE_DIR)

SECRET_KEY = 'h=__c_&zzx)d8ko8*6_8@(q2^*gm7-977m%0wgr51@&mjh53h$'

DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

AUTHENTICATION_BACKENDS = [
    'secure_auth.base.backends.ManualModelBackend',
    'django.contrib.auth.backends.ModelBackend'
]

ROOT_URLCONF = 'secure_auth.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'secure_auth.wsgi.application'


# Internationalization

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'public', 'media')

STATIC_ROOT = os.path.join(PROJECT_DIR, 'public', 'static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)


# Session

SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 4

SESSION_COOKIE_DOMAIN = None

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


# Installed apps

INSTALLED_APPS += (
    'secure_auth.base',
)

# ==============================================================================
# Logging
# ==============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_DIR, 'debug.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'secure_auth.apps': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'secure_auth.base': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


# Production settings
if os.environ.get('ENV') == 'production':
    from .production import *  # noqa

# Develop settings
elif os.environ.get('ENV') == 'develop':
    from .develop import *  # noqa

# Staging settings
elif os.environ.get('ENV') == 'staging':
    from .staging import *  # noqa

# Default choice
else:
    from .develop import *  # noqa

# Local settings
try:
    from .local import *  # noqa
except ImportError:
    pass
