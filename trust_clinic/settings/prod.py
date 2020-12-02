from .base import *

DEBUG = False
ALLOWED_HOSTS = ['*']

INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic')
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
