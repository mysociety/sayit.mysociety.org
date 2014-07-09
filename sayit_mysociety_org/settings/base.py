# Django settings for sayit_mysociety_org project.

import imp
import os
import sys
from django.conf import global_settings
from .paths import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_TOOLBAR = True
DEBUG_TOOLBAR_PATCH_SETTINGS = False

ALLOWED_HOSTS = [ '.sayit.mysociety.org' ]

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PARENT_DIR, 'sqlite.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'locale'),
)

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PARENT_DIR, 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# All uploaded files world-readable
FILE_UPLOAD_PERMISSIONS = 0644

# List of callables that know how to import templates from various sources.
loaders = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'apptemplates.Loader',
#     'django.template.loaders.eggs.Loader',
)
if not DEBUG:
    loaders = ( ('django.template.loaders.cached.Loader', loaders), )

TEMPLATE_LOADERS = loaders

MIDDLEWARE_CLASSES = [
    'django.middleware.gzip.GZipMiddleware',
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'instances.middleware.MultiInstanceMiddleware',
    'sayit_mysociety_org.middleware.WhoDidMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

INTERNAL_IPS = ( '127.0.0.1', )

ROOT_URLCONF = 'sayit_mysociety_org.urls'
ROOT_URLCONF_HOST = 'sayit_mysociety_org.urls-host'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'sayit_mysociety_org.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",
    "sayit_mysociety_org.context_processors.add_settings",
    "sayit_mysociety_org.context_processors.nav_section",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.twitter',
    'haystack',
    'south',
    'django_select2',
    'tastypie',
    'django_bleach',
    'pipeline',
    'popit',
    'popolo',
    'instances',
    'speeches',
    'about',
    'login_token',
]

try:
    # Find rather than import, as that circular imports settings
    imp.find_module('django_nose')
    INSTALLED_APPS.append('django_nose')
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
except:
    pass

# Log WARN and above to stderr; ERROR and above by email when DEBUG is False.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': [ 'mail_admins', 'console' ],
            'level': 'WARN',
            'propagate': True,
        },
        'speeches': {
            'handlers': [ 'mail_admins', 'console' ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'pyelasticsearch': {
            'handlers': ['console'],
            'level': 'WARN',
            'propagate': True,
        },
        'requests.packages.urllib3.connectionpool': {
            'handlers': ['console'],
            'level': 'WARN',
            'propagate': True,
        },
    }
}

# pagination related settings
PAGINATION_DEFAULT_PAGINATION = 10
PAGINATION_DEFAULT_WINDOW = 2
PAGINATION_DEFAULT_ORPHANS = 2
PAGINATION_INVALID_PAGE_RAISES_404 = True

APPEND_SLASH = False

# South
# Don't use migrations in testing - makes things faster and avoids
# errors with difference between sqlite and postgres
SOUTH_TESTS_MIGRATE = False

AUTHENTICATION_BACKENDS = (
    'login_token.auth_backend.LoginTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_EMAIL_REQUIRED = False

# XXX This should be the user's profile page once such things exist
LOGIN_REDIRECT_URL = '/'

# Select2
AUTO_RENDER_SELECT2_STATICS = False

# Now get the mySociety configuration
from .mysociety import *

# django-pipeline and static file configuration
from .pipeline import *

# django-bleach configuration
from .bleach import *

# Cookies, after because we need BASE_HOST from mysociety.py
SESSION_COOKIE_DOMAIN = BASE_HOST
SESSION_COOKIE_NAME = 's'

SEARCH_INDEX_NAME = DATABASES['default']['NAME']
if 'test' in sys.argv:
    SEARCH_INDEX_NAME += '_test'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'sayit_mysociety_org.search.backends.SayitElasticSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': SEARCH_INDEX_NAME,
    },
    'write': {
        'ENGINE': 'sayit_mysociety_org.search.backends.SayitElasticSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': '%s_write' % SEARCH_INDEX_NAME,
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

if DEBUG:
    cache = { 'BACKEND': 'django.core.cache.backends.dummy.DummyCache' }
    CACHE_MIDDLEWARE_SECONDS = 0
else:
    cache = {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': DATABASES['default']['NAME'],
    }
    CACHE_MIDDLEWARE_SECONDS = 3600

CACHES = {
    'default': cache
}

if DEBUG_TOOLBAR:
    MIDDLEWARE_CLASSES.append( 'debug_toolbar.middleware.DebugToolbarMiddleware' )
    INSTALLED_APPS.append( 'debug_toolbar' )
