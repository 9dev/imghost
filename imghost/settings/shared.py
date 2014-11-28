import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
        
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.tumblr',
    'allauth.socialaccount.providers.twitter',
    
    'crispy_forms',
    'taggit',
    'kronos',
    'imagekit',
    'guardian',
    'haystack',
    'sorl.thumbnail',
    'captcha',
    'agon_ratings',
    'dialogos',
    
    'oembed9',
    
    'main',
    
    'django_cleanup', # must be after the other apps
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

TEMPLATE_CONTEXT_PROCESSORS += (
    "django.core.context_processors.request", # required by allauth template tags
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend", # required in order to login by username in Django admin, regardless of django-allauth # also required by django-guardian
    "allauth.account.auth_backends.AuthenticationBackend",   
    'guardian.backends.ObjectPermissionBackend',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr',
    },
}

ROOT_URLCONF = 'imghost.urls'
WSGI_APPLICATION = 'imghost.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR))) + '/static'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SITE_ID = 1

LOGIN_REDIRECT_URL = '/'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_USERNAME_BLACKLIST = ['admin']

ANONYMOUS_USER_ID = -1 # required by django-guardian and sitemaps
GUARDIAN_RENDER_403 = True

RESULTS_PER_PAGE = 5
HAYSTACK_SEARCH_RESULTS_PER_PAGE = RESULTS_PER_PAGE

OEMBED9_PROVIDER_NAME = 'Imghost'
OEMBED9_CACHE_AGE = 31536000

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache',
    }
}

ADMINS = ('admin', 'some_account@gmail.com')

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'some_account@gmail.com'
EMAIL_HOST_PASSWORD = 'some_password'

RECAPTCHA_PUBLIC_KEY = 'XXX'
RECAPTCHA_PRIVATE_KEY = 'YYY'


