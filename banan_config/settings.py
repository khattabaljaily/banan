"""
Django settings for banan_config project (Banan Information Technology website).
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / 'secrets.json') as secrets_file:
    secrets = json.load(secrets_file)

SECRET_KEY = secrets['SECRET_KEY']
DEBUG = secrets['DEBUG']
ALLOWED_HOSTS = secrets['ALLOWED_HOSTS']
SITE_URL = secrets.get('SITE_URL', 'https://banantechnology.com')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'banan_config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_meta',
            ],
        },
    },
]

WSGI_APPLICATION = 'banan_config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

DATABASES = {
    'default': secrets['DATABASE']
}

if DATABASES['default']['ENGINE'].endswith('sqlite3'):
    DATABASES['default']['NAME'] = BASE_DIR / DATABASES['default']['NAME']


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', 'English'),
    ('ar', 'العربية'),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

TIME_ZONE = 'Asia/Qatar'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Content-hashed static filenames (e.g. style.3b82f1a9.css) so an edited file
# gets a brand-new URL instead of relying on a "?v=" query string for cache
# busting — some mobile carrier proxies cache by path only and strip query
# strings, which can serve a stale (and in this project's case, once-broken)
# CSS/JS file indefinitely regardless of what the origin serves.
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage',
    },
}

# Media files (user uploads: portfolio project images, etc.)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Site info used across templates (also see core/context_processors.py)
COMPANY_NAME = 'Banan Information Technology'
COMPANY_NAME_AR = 'بنان لتقنية المعلومات'
COMPANY_CR_NUMBER = '247136'
COMPANY_PHONE = '+974 3393 3700'
COMPANY_PHONE_TEL = '+97433933700'
COMPANY_EMAIL = 'info@banantechnology.com'
COMPANY_ADDRESS = 'Doha, Qatar'

# Toggle to show/hide the "Work" (portfolio) nav link once case studies are ready.
# The /portfolio/ page and URLs stay live either way — this only hides the nav entry.
SHOW_WORK_NAV = True

# Toggle to show/hide the "Products" nav link (Banan IMS and future in-house products).
SHOW_PRODUCTS_NAV = True

# Social profiles
SOCIAL_FACEBOOK_URL = 'https://facebook.com/banantechnology'
SOCIAL_INSTAGRAM_URL = 'https://instagram.com/banantechnology'


# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration
# Falls back to printing to the console in DEBUG so local development doesn't
# need real SMTP credentials; set DEBUG=false in secrets.json to send for real.

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'mail.privateemail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = 10
EMAIL_HOST_USER = secrets['EMAIL']['HOST_USER']
EMAIL_HOST_PASSWORD = secrets['EMAIL']['HOST_PASSWORD']
DEFAULT_FROM_EMAIL = f'Banan Information Technology <{EMAIL_HOST_USER}>'
SERVER_EMAIL = EMAIL_HOST_USER
CONTACT_EMAIL_RECIPIENT = COMPANY_EMAIL

ADMINS = [('Khattab', 'khattabaljaily@gmail.com')]
MANAGERS = ADMINS


# Logging
# Errors also get emailed to ADMINS (see mail_admins handler below) once SMTP
# is configured for real, on top of the rotating file.

(BASE_DIR / 'logs').mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {name} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'verbose',
            'level': 'WARNING',
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}


# Transport security
# Left off under DEBUG so local http:// development still works.

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
