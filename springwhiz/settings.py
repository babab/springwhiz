# Copyright (C) 2012-2013  Benjamin Althues
#
# This file is part of springwhiz.
#
# springwhiz is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# springwhiz is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with springwhiz.  If not, see <http://www.gnu.org/licenses/>.

import os.path
import sys

try:
    import settings_local
except ImportError:
    print 'Move example.settings_local.py -> settings_local.py and edit it'
    sys.exit(1)

DEPLOY_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SPRINGWHIZ_VERSION = '0.6.0-dev'
DEBUG = settings_local.DEBUG
TEMPLATE_DEBUG = settings_local.TEMPLATE_DEBUG
ADMINS = settings_local.ADMINS
BASE_URL = settings_local.BASE_URL
DATABASES = settings_local.DATABASES
TIME_ZONE = settings_local.TIME_ZONE
LANGUAGE_CODE = settings_local.LANGUAGE_CODE
SITE_ID = settings_local.SITE_ID
USE_I18N = settings_local.USE_I18N
USE_L10N = settings_local.USE_L10N
USE_TZ = settings_local.USE_TZ
SECRET_KEY = settings_local.SECRET_KEY
STATIC_ROOT = settings_local.STATIC_ROOT
STATIC_URL = settings_local.STATIC_URL
ALLOWED_HOSTS = settings_local.ALLOWED_HOSTS
SUBDIRECTORY_USE = settings_local.SUBDIRECTORY_USE
SUBDIRECTORY_PATH = settings_local.SUBDIRECTORY_PATH

MANAGERS = ADMINS

if SUBDIRECTORY_USE:
    LOGIN_URL = '{0}accounts/login/'.format(SUBDIRECTORY_PATH)
    LOGOUT_URL = '{0}accounts/logout/'.format(SUBDIRECTORY_PATH)
    LOGIN_REDIRECT_URL = SUBDIRECTORY_PATH
else:
    LOGIN_URL = '/accounts/login/'
    LOGOUT_URL = '/accounts/logout/'
    LOGIN_REDIRECT_URL = '/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Additional locations of static files
STATICFILES_DIRS = (
    '%s/static' % DEPLOY_PATH,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'springwhiz.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'springwhiz.wsgi.application'

TEMPLATE_DIRS = (
    '%s/springwhiz/tpl' % DEPLOY_PATH
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.markup',
    'springwhiz.bookmarks',
    'springwhiz.notepad',
    'springwhiz.tyd',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'springwhiz.context_processors.platform_version_info',
    'springwhiz.context_processors.base_url',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
