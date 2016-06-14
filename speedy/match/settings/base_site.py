from speedy.net.settings.base import *

from .utils import APP_DIR

SITE_NAME = 'Speedy Match'

SITE_URL = env('SPEEDY_MATCH_URL')

ROOT_URLCONF = 'speedy.match.urls'

STATIC_ROOT = str(APP_DIR / 'static_serve')

TEMPLATES[0]['DIRS'].insert(0, str(APP_DIR / 'templates'))

STATICFILES_DIRS.insert(0, str(APP_DIR / 'static'))

INSTALLED_APPS += [
    'speedy.match.accounts',
]

AUTH_PROFILE_MODEL = 'match_accounts.SiteProfile'
