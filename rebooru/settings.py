import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


DEBUG = False
TEMPLATE_DEBUG = DEBUG

# admins/dbs/allowed hosts are left blank in the main settings
# define them in local_settings instead
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

ALLOWED_HOSTS = []

# end local_settings override stuff, the rest is okay defaults

TIME_ZONE = 'America/Los_Angeles'

LANGUAGE_CODE = 'en-us'

# leave out translation stuff, but include timezone/number stuff
USE_I18N = False
USE_L10N = True
USE_TZ = True

# urls for things
ROOT_URLCONF = 'rebooru.urls'
STATIC_URL = '/static/'
MEDIA_URL = STATIC_URL + 'media/'

# set root directories to match the urls and PROJECT_ROOT
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip('/'))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip('/').split('/'))
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, 'templates'),)

# our own user model
AUTH_USER_MODEL = 'accounts.Account'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

WSGI_APPLICATION = 'rebooru.wsgi.application'

INSTALLED_APPS = (
    # stock django stuff
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    # third-party stuff
    'south',

    # rebooru stuff
    'rebooru.apps.core',
    'rebooru.apps.accounts',
    'rebooru.apps.images',
)

# default logging setup, which emails ADMINS with 500 errors
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# SECRET_KEY machinery: if it's not defined in local_settings.py or
# secret_key.py, generate a new one and put it in secret_key.py
# the reason this isn't just outright defined is as a convenience if anyone
# sets up their own server for this in the future

SECRET_KEY = None

from local_settings import *

# still no key?
if not SECRET_KEY:
    try:
        # grab it from the file, unless there isn't one
        from secret_key import *
    except ImportError:
        # there's no secret_key.py and SECRET_KEY isn't in local_settings.py
        # so let's make one. this is how django makes one
        from django.utils.crypto import get_random_string
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        SECRET_KEY = get_random_string(50, chars)

        # and now that we have it, we can write it to a file for future use
        keyfile = open(os.path.join(PROJECT_ROOT, 'secret_key.py'), 'w')
        keyfile.write("SECRET_KEY = '%s'\n" % SECRET_KEY)
        keyfile.close()
