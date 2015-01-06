"""
Django settings for heroku_demo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DEBUG_TEMPLATE = True

ROOT_URLCONF = 'heroku_demo.urls'

WSGI_APPLICATION = 'heroku_demo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Parse database configuration from $DATABASE_URL
#DATABASES['default'] =  dj_database_url.config()

# Enable Connection Pooling (if desired)
#DATABASES['default']['ENGINE'] = 'django_postgrespool'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# *************************************************************************
# *************************************************************************
# **************************** django-dash setup **************************
# *************************************************************************
# *************************************************************************

PROJECT_DIR = lambda base: os.path.abspath(
    os.path.join(os.path.dirname(__file__), base).replace('\\', '/')
)
gettext = lambda s: s

DEBUG_TOOLBAR = False

LANGUAGES = (
    ('en', gettext("English")),  # Main language!
    ('hy', gettext("Armenian")),
    ('nl', gettext("Dutch")),
    ('ru', gettext("Russian")),
)

SITE_ID = 1

MEDIA_ROOT = PROJECT_DIR('media')

MEDIA_URL = '/media/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'APP_DIRS': True,
        'DIRS': [PROJECT_DIR(os.path.join('..', 'templates'))],
        'OPTIONS': {
            'context_processors': [
                "django.template.context_processors.debug",
                'django.template.context_processors.request',
                "django.contrib.auth.context_processors.auth",
                # "django.core.context_processors.i18n",
                # "django.core.context_processors.media",
                # "django.core.context_processors.static",
                # "django.core.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                # 'django.template.loaders.eggs.Loader',
                'admin_tools.template_loaders.Loader',
            ],
            'debug': DEBUG_TEMPLATE,
        }
    },
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

INSTALLED_APPS = (
    # Admin dashboard
    'admin_tools',
    'admin_tools.menu',

    # Django core and contrib apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.sitemaps',

    # Third party apps used in the project
    'tinymce',  # TinyMCE
    'django_registration',  # Auth views and registration app
    'easy_thumbnails',  # Thumbnailer

    # Dash core, contrib layouts and apps
    'dash',  # Dash core
    'dash.contrib.layouts.android',  # Android layout for Dash
    'dash.contrib.layouts.bootstrap2',  # Bootstrap 2 layouts for Dash
    'dash.contrib.layouts.windows8',  # Windows 8 layout for Dash
    'dash.contrib.plugins.dummy',  # Dummy (testing) plugin for Dash
    'dash.contrib.plugins.memo',  # Memo plugin for Dash
    'dash.contrib.plugins.image',  # Image plugin for Dash
    'dash.contrib.plugins.rss_feed',  # RSS feed plugin for Dash
    'dash.contrib.plugins.url',  # URL plugin for Dash
    'dash.contrib.plugins.video',  # Video plugin for Dash
    'dash.contrib.plugins.weather',  # Weather plugin for Dash
    'dash.contrib.apps.public_dashboard',  # Public dashboard app for Dash

    # Other project specific apps
    # 'admin_tools_dashboard', # Admin dashboard
    'foo',  # Test app
    'bar',  # Another test app
    'd3_samples',  # Sample D3 plugins
    'news',  # Sample news plugin for Dash
    # 'customauth', # Custom user model
)


LOGIN_REDIRECT_URL = '/dashboard/'
LOGIN_URL = '/accounts/login/'
LOGIN_ERROR_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'

# django-admin-tools custom dashboard
ADMIN_TOOLS_MENU = 'admin_tools_dashboard.menu.CustomMenu'

ACCOUNT_ACTIVATION_DAYS = 2


if DEBUG and DEBUG_TOOLBAR:
    try:
        # Make sure the django-debug-toolbar is installed
        import debug_toolbar

        # debug_toolbar
        MIDDLEWARE += (
            'debug_toolbar.middleware.DebugToolbarMiddleware',
        )

        INSTALLED_APPS += (
            'debug_toolbar',
        )

        DEBUG_TOOLBAR_CONFIG = {
            'INTERCEPT_REDIRECTS': False,
        }

    except ImportError:
        pass

try:
    from .local_settings import *
except ImportError as e:
    pass
