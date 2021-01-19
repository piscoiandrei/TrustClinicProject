import os
from pathlib import Path
import django_heroku

# Note: default is parent.parent to go to the main dir now
# we need to go one level higher
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False
ALLOWED_HOSTS = ['trustclinic.herokuapp.com']

INSTALLED_APPS = [
    # installed
    'channels',

    # my apps
    'accounts',
    'visitor',
    'generic',
    'chat',
    'client',
    'doctor',

    # installed
    'crispy_forms',
    'bootstrap_admin',

    # default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # installed
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'trust_clinic.middleware.FooterDynamicData',
    'trust_clinic.middleware.LoginRequired',
]

ROOT_URLCONF = 'trust_clinic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'trust_clinic.wsgi.application'

AUTH_USER_MODEL = 'accounts.User'

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

PASSWORD_HASHERS = [
    'trust_clinic.hashers.BCrypt10x',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

# ASGI CONFIG
ASGI_APPLICATION = 'trust_clinic.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get("REDIS_URL")],
        },
    },
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Bucharest'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
# auth
LOGGED_OUT_ONLY_URLS = [
    '/',
    'visitor/',
    'accounts/login/',
    'accounts/register/',
    'accounts/password_reset/',
    'accounts/password_reset/done/',
    'accounts/reset/',
    'accounts/reset/done/'
]
# no permissions in order to access these urls
LOGIN_REQUIRED_URLS = [
    'accounts/logout/',
]
# specific permissions required to access these urls
CLIENT_URLS = [
    'accounts/edit-profile/',
    'accounts/change-password/',
    'accounts/change-password-done/',
    'chat/client/',
    'client/dashboard/',
    'client/specializations/',
    'client/specialization/detail/',
    'client/doctors/',
    'client/doctor/detail/',
    'client/clinics/',
    'client/clinics/detail/',
    'client/schedule/',
    'client/appointments/',
    'client/appointment/success/',
    'client/appointment/delete/confirm/',
    'client/appointment/delete/',
    'client/appointment/delete/done/',
]
OPERATOR_URLS = [
    'chat/operator/',
]
DOCTOR_URLS = [
    'doctor/dashboard/',
    'doctor/appointment/delete/',
    'doctor/working-hours/',
]

LOGIN_REDIRECT_URL = 'accounts/login/'
LOGIN_URL = 'accounts/login/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# SMTP CONFIG
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_SIGNATURE_VERSION = 's3v4'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

django_heroku.settings(locals())
