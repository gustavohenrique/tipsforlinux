# -*- coding:utf-8 -*-
import os
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('TipsForLinux', 'tipsforlinux@tipsforlinux.com'),
    ('Gustavo Henrique', 'gustavo@gustavohenrique.net'),
)

# Used by contact-form
MANAGERS = ADMINS

#DATABASE_ENGINE = 'sqlite3'
#DATABASE_NAME = os.path.join(PROJECT_ROOT_PATH, 'tipsforlinux.db')
#DATABASE_USER = ''
#DATABASE_PASSWORD = ''
#DATABASE_HOST = ''
#DATABASE_PORT = ''

MEDIA_ROOT = os.path.join(PROJECT_ROOT_PATH, 'media')

TIME_ZONE = 'America/Sao_Paulo'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1
USE_I18N = True

SECRET_KEY = 's-cf9xrjk@kzpe*)5k3%2vk@(+rankt6h4%+3*%k3+#p^sl5h*'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'openid_consumer.middleware.OpenIDMiddleware',
    'middleware.threadlocals.ThreadLocals',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'socialauth.middleware.FacebookConnectMiddleware'
    'pagination.middleware.PaginationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    #"socialauth.context_processors.facebook_api_key",
    'django.core.context_processors.media',
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "tips.context_processors.menu",
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT_PATH, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.sitemaps',
    'robots',
    'socialauth',
    'openid_consumer',
    'tagging',
    'pagination',
    'tips',
    'contact_form',
)

DATE_FORMAT = '%d/%m/%Y'
DATETIME_FORMAT = 'd/m/Y - H:i:s'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Default vars in separateds settings files
MAIL_TO_RECEIVE_POSTS_UPDATES = ''
#EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
#EMAIL_PORT = '587'
DEFAULT_FROM_EMAIL = ''

AKISMET_API_KEY = ''

TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''

SITE_NAME = 'localhost'

ROBOTS_SITEMAP_URL = '/sitemap.xml'

# Imports according of hostname
import socket
hostname = socket.gethostname()
if 'webfaction' in hostname:
    from settings_prod import *
else:
    from settings_dev import *

from settings_auth import *

