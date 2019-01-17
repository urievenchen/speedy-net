# ~~~~ TODO: remove unnecessary comments.
"""
Django settings for speedy project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

from django.utils.translation import gettext_lazy as _

from .utils import env, APP_DIR, ROOT_DIR


SPEEDY_NET_SITE_ID = int(env('SPEEDY_NET_SITE_ID'))
SPEEDY_MATCH_SITE_ID = int(env('SPEEDY_MATCH_SITE_ID'))
SPEEDY_COMPOSER_SITE_ID = int(env('SPEEDY_COMPOSER_SITE_ID'))
SPEEDY_MAIL_SOFTWARE_SITE_ID = int(env('SPEEDY_MAIL_SOFTWARE_SITE_ID'))

SITES_WITH_LOGIN = [
    SPEEDY_NET_SITE_ID,
    SPEEDY_MATCH_SITE_ID,
]

XD_AUTH_SITES = SITES_WITH_LOGIN

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

DEFAULT_FROM_EMAIL = 'webmaster@speedy.net'

ADMINS = MANAGERS = (
    ('Uri Rodberg', 'webmaster@speedy.net'),
)

USE_SSL = False

# Application definition

INSTALLED_APPS = [
    'modeltranslation',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms',
    'friendship',
    'rules.apps.AutodiscoverRulesConfig',
    'sorl.thumbnail',

    'speedy.core.base',
    # 'speedy.core.accounts',
    # 'speedy.core.im',
    # 'speedy.core.profiles',
    # 'speedy.core.friends',
    # 'speedy.core.blocks',
    # 'speedy.core.uploads',
    # 'speedy.core.feedback',
]

MIDDLEWARE = [
    'speedy.core.base.middleware.SessionCookieDomainMiddleware',
    'speedy.core.base.middleware.RemoveExtraSlashesMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    'speedy.core.base.middleware.LocaleDomainMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'speedy.core.accounts.middleware.SiteProfileMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(APP_DIR / 'templates'),
            str(ROOT_DIR / 'speedy/core/templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',

                'speedy.core.base.context_processors.active_url_name',
                'speedy.core.base.context_processors.settings',
                'speedy.core.base.context_processors.sites',
                'speedy.core.base.context_processors.speedy_net_domain',
                'speedy.core.base.context_processors.speedy_match_domain',
            ],
        },
    },
]

# USER_PROFILE_WIDGETS = [
#     'speedy.core.profiles.widgets.UserPhotoWidget',
#     'speedy.core.profiles.widgets.UserInfoWidget',
# ]
#
CRISPY_TEMPLATE_PACK = 'bootstrap4'

CRISPY_FAIL_SILENTLY = False

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': env.db()
}

CACHES = {
    'default': env.cache()
}

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

# MIN_PASSWORD_LENGTH = 8
# MAX_PASSWORD_LENGTH = 120
#
# PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'speedy.core.accounts.validators.PasswordMinLengthValidator',
#     },
#     {
#         'NAME': 'speedy.core.accounts.validators.PasswordMaxLengthValidator',
#     },
# ]
#
# AUTH_PASSWORD_VALIDATORS = PASSWORD_VALIDATORS
#
# ~~~~ TODO: remove
# AUTH_PASSWORD_VALIDATORS = []
#
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

DEFAULT_AUTHENTICATION_BACKEND = 'django.contrib.auth.backends.AllowAllUsersModelBackend'

AUTHENTICATION_BACKENDS = (
    'rules.permissions.ObjectPermissionBackend',
    DEFAULT_AUTHENTICATION_BACKEND,
)

SESSION_COOKIE_AGE = int(60 * 60 * 24 * 365.25 * 30)  # ~ 30 years

# AUTH_USER_MODEL = 'accounts.User'
#
# LOGIN_URL = '/login/'
#
# LOGIN_REDIRECT_URL = '/me/'
#
# XD_AUTH_SITES = [
#     SPEEDY_NET_SITE_ID,
#     SPEEDY_MATCH_SITE_ID,
# ]
#
# UNAVAILABLE_USERNAMES = [
#     'admin', 'root', 'webmaster', 'uri', 'speedy',
#     'register', 'login', 'logout', 'me', 'editprofile', 'resetpassword',
#     'friends', 'messages', 'feedback', 'contact', 'about', 'i18n',
#     'welcome', 'setsession', 'static', 'images', 'icons', 'css', 'js',
#     'javascript', 'python',
#     'speedynet', 'speedymatch', 'speedycomposer', 'speedymail', 'speedymailsoftware',
#     'postmaster', 'mail', 'domain', 'locale',
# ]
#
# DONT_REDIRECT_INACTIVE_USER = [
#     '/logout/',
#     '/welcome/',
#     '/registration-step-',
#     '/about/',
#     '/privacy/',
#     '/terms/',
#     '/contact/',
#     '/edit-profile/',
#     '/admin/',
#     '/media/',
#     '/static/',
#     '/set-session/',
# ]
#

SMALL_UDID_LENGTH = 15
REGULAR_UDID_LENGTH = 20

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', _('English')),
    ('he', _('Hebrew')),
]

# Canceled - we don't need this list, we can just do `for language_code, language_name in django_settings.LANGUAGES`.
# ALL_LANGUAGE_CODES = [language_code for language_code, language_name in LANGUAGES]

LOCALE_PATHS = [
    str(APP_DIR / 'locale'),
    str(ROOT_DIR / 'speedy/core/locale'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    str(APP_DIR / 'static'),
    str(ROOT_DIR / 'speedy/core/static')
]

# Media files (user uploads)

MEDIA_URL = '/media/'

MEDIA_ROOT = str(ROOT_DIR / 'media')

THUMBNAIL_DEBUG = True

THUMBNAIL_DUMMY = True

# Tests

TEST_RUNNER = 'speedy.core.base.test.models.SiteDiscoverRunner'

# ~~~~ TODO: remove
# SITE_PROFILES = {
#     'net': {
#         'site_profile_model': 'net_accounts.SiteProfile',
#     },
#     'match': {
#         'site_profile_model': 'match_accounts.SiteProfile',
#     }
# }
#
FIXTURE_DIRS = [
    str(ROOT_DIR / 'speedy/core/fixtures')
]

# SITE_PROFILE_ACTIVATION_FORM = 'speedy.core.accounts.forms.SiteProfileActivationForm'
#
MODELTRANSLATION_ENABLE_FALLBACKS = False


# ~~~~ TODO: check if this is good for production!
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
#         'verbose': {
# #            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#             'format': '%(asctime)s %(name)s %(levelname)s: %(message)s',
#             'datefmt': '%Y-%m-%d %H:%M:%S',
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
    },
    'handlers': {
        # 'file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'filename': '/var/log/speedy_net_django.log',
        #     'formatter': 'verbose',
        # },
        'syslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'local7',
            'address': '/dev/log',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'root': {
            'handlers': ['syslog', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['syslog', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['syslog', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['syslog', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'speedy': {
            'handlers': ['syslog', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # 'speedy.net': {
        #     'handlers': ['syslog', 'mail_admins'],
        #     'level': 'DEBUG',
        #     'propagate': True,
        # },
        # 'speedy.match': {
        #     'handlers': ['syslog', 'mail_admins'],
        #     'level': 'DEBUG',
        #     'propagate': True,
        # },
        # 'speedy.composer': {
        #     'handlers': ['syslog', 'mail_admins'],
        #     'level': 'DEBUG',
        #     'propagate': True,
        # },
        # 'speedy.mail': {
        #     'handlers': ['syslog', 'mail_admins'],
        #     'level': 'DEBUG',
        #     'propagate': True,
        # },
    },
}


