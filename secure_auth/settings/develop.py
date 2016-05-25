# -*- coding: utf-8 -*-
"""
    Настройки среды для разработки
"""
from . import *


SITE_ID = 1

DEBUG = True

COMPRESS_ENABLED = not DEBUG

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'secure_auth.db')
    }
}

INSTALLED_APPS += (
    'debug_toolbar',
)
