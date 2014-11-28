try:
    from shared import *
except ImportError:
    pass

import os

SECRET_KEY = 'p@d-+#5_x%2m--5$0b=j^7!@$qk+0y0li)yn76al+yjt)_-%w@'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

ALLOWED_HOSTS = []

INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',
)

OEMBED9_PROVIDER_URL = 'http://127.0.0.1:8000'
