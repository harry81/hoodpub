import os
from datetime import timedelta
gettext = lambda s: s
DATA_DIR = os.path.dirname(os.path.dirname(__file__))

"""
Django settings for main project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5na+q+@*3v8^8&vm1iv=z^vod=1+=dz_ntrnk74x^b8vktgw*s'

DEBUG = True

if os.path.isdir('/home/deploy/'):
    DEBUG = False

# SECURITY WARNING: don't run with debug turned on in production!
ADMINS = (('John', 'chharry@gmail.com'),)
ALLOWED_HOSTS = [u'.dev.hoodpub.com', '.hoodpub.com',
                 'hoodpub.com']


TEMPLATE_DEBUG = True
# Application definition

TEMPLATE_DIRS = (
    "%s/templates" % BASE_DIR,
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
    'templated_email',
    'oauth2_provider',
    'rest_framework_swagger',
    'social.apps.django_app.default',
    'rest_framework_social_oauth2',
    'django_extensions',
    'threadedcomments',
    'django_comments',
    'django.contrib.sites',
    'rest_framework',
    "compressor",
    'constance',
    'djcelery',
    'book',
    'hoodpub',
    'hoodpub_auth',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'main.urls'

WSGI_APPLICATION = 'main.wsgi.application'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ),
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
STATIC_ROOT = os.path.join(DATA_DIR, 'static')

COMMENTS_APP = 'threadedcomments'
SITE_ID = 1

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
TEMPLATED_EMAIL_BACKEND =\
    'templated_email.backends.vanilla_django.TemplateBackend'

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_EXPIRATION_DELTA': timedelta(seconds=2592000),
}

PROPRIETARY_BACKEND_NAME = 'Facebook'

BROKER_URL = 'amqp://guest:guest@www.hoodpub.com:5672//'
CELERY_RESULT_BACKEND = "amqp"
CELERY_SEND_TASK_ERROR_EMAILS = True

import djcelery
djcelery.setup_loader()

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

CONSTANCE_REDIS_CONNECTION = {
    'host': 'redis',
    'port': 6379,
    'db': 0,
}

try:
    from settings_local import *
except ImportError:
    pass
