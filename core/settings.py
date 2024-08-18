# -*- encoding: utf-8 -*-

import os
# from decouple import config
from unipath import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_1122')
SECRET_KEY = 'S#perS3crEt_1122'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config('DEBUG', default=True, cast=bool)
DEBUG = True

LL = {'CRITICAL': 50,
      'ERROR': 40,
      'WARNING': 30,
      'INFO': 20,
      'NOTSET': 0}

LOG_LEVEL = LL['INFO']

ALLOWED_HOSTS = ["www.inpost.su", "inpost.su", "85.209.9.148"]  # inpost.su, 85.209.9.148

CSRF_TRUSTED_ORIGINS = ["https://inpost.su"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.home',
    'apps.spamer',

    'crispy_forms',
    # 'filer',
    'mptt',
    'easy_thumbnails',
    'debug_toolbar',
    # 'emoji_picker',
    'markitup',
    'django_quill',
]

CRISPY_TEMPLATE_PACK = 'uni_form'

MARKITUP_FILTER = ('markdown.markdown', {})
MARKITUP_AUTO_PREVIEW = False

QUILL_CONFIGS = {
    'default': {
        'theme': 'snow',
        'modules': {
            'syntax': True,
            'toolbar': [
                [
                    # {'font': []},
                    # {'header': []},
                    # {'align': []},
                    'bold', 'italic', 'underline', 'strike',
                    # {'color': []},
                    # {'background': []},
                ],
                [
                    # 'code-block',
                    'link'
                ],
                # ['clean'],
            ]
        }
    }
}

MIDDLEWARE = [
    'apps.spamer.middleware.BlockDomainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.middleware.current_user.CurrentUserMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# def show_toolbar(request):
#     return True
# DEBUG_TOOLBAR_CONFIG = {
#     "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
# }

INTERNAL_IPS = [
    "127.0.0.1:443",
    "85.209.9.148",
]

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "home"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in home/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'apps.home.context_processors.get_notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
if os.name == 'nt':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/var/www/html/inpost/db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525
EMAIL_HOST_USER = "tgmail_no_reply@inbox.ru"
EMAIL_HOST_PASSWORD = "DvpKvv4NQpQiTtkdVE7E"
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = True

SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_L10N = True

USE_TZ = False

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, "static/media")

MEDIA_URL = '/media/'
MEDIA_URL_TG = '/media/sessions/downolads/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
