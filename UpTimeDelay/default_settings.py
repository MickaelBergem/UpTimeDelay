#-*- coding: utf-8 -*-
"""
Default local setting file, create a `local_settings.py` file along me to customize the variables !
"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(l^bn*x&31vy3lyu9ceskz8dec^yue99u_^c*iyczz7g1$a430'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Path to PING command
PING_CMD = '/usr/bin/ping'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Applications locally installed
LOCAL_APPS = (
    'debug_toolbar',
)
