# Copyright 2011 Terena. All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:

#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.

#    2. Redistributions in binary form must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in the documentation
#        and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY TERENA ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL TERENA OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies,
# either expressed or implied, of Terena.

# Django settings for peer project.

import datetime
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = 'no-reply@example.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'peer',                      # Or path to database file if using sqlite3.
        'USER': 'peer',                      # Not used with sqlite3.
        'PASSWORD': 'peer',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASEDIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASEDIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASEDIR, 'staticfiles'),
)

# Aditional theme custom styles 
PEER_THEME = {
    'LINK_COLOR': '#5669CE',
    'LINK_HOVER': '#1631BC',
    'HEADING_COLOR': '#1631BC',
    'INDEX_HEADING_COLOR': '#ff7b33',
    'HEADER_BACKGROUND': '',
    'CONTENT_BACKGROUND': '',
    'FOOTER_BACKGROUND': '',
    'HOME_TITLE': 'Nice to meet you!!',
    'HOME_SUBTITLE': 'Say hello to federated worldwide services',
    'JQUERY_UI_THEME': 'default-theme',
}

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


# List of processors used by RequestContext to populate the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
#    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'peer.portal.context_processors.peer_theme',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'peer.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASEDIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'registration',
    'south',
    'djangosaml2',
    'peer.account',
    'peer.domain',
    'peer.entity',
    'peer.portal',
)

# needed for django-registration
ACCOUNT_ACTIVATION_DAYS = 2
LOGIN_REDIRECT_URL = '/'

# Email settings. Commented by security, but should be rewrite on a local or production settings
# EMAIL_HOST = 'smtp.example.com'
# EMAIL_PORT = 25

# reCaptcha keys. Not filled for security
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

# ENTITY METADATA VALIDATION
METADATA_VALIDATORS = (
    'peer.entity.validation.validate_xml_syntax',
    'peer.entity.validation.validate_domain_in_endpoints',
    'peer.entity.validation.validate_metadata_permissions',
#    'peer.entity.validation.validate_domain_in_entityid',
)

# Permissions for metadata attribute. The metadata attribute is defined by
# its XPATH. The triplets are (<XPATH>, <Permission name>, <Permission
# description>) 
METADATA_PERMISSIONS = (
    ('/md:EntityDescriptor', 'entity_descriptor', 'Entity Descriptor'),
    ('.//md:ServiceDescription', 'service_descriptor', 'Service Description'),
    ('.//mdui:Description', 'description', 'Description'),
    ('.//md:OrganizationName', 'organization_name', 'Organization Name'),
)

# VFF VERSIONED FILE BACKEND
VERSIONEDFILE_BACKEND = 'vff.git_backend.GitBackend'

# POSTGRESQL FULL TEXT SEARCH

# What language to use for full text searches (only Postgresql)
PG_FT_INDEX_LANGUAGE = u'english'

# If the user enters various terms in a serch, do we join them
# with OR or with AND
# PG_FTS_OPERATOR = u'|'
PG_FTS_OPERATOR = u'&'

# SAMLmetaJS plugins
SAML_META_JS_PLUGINS = ('info', 'org', 'contact', 'saml2sp', 'certs',
                        'attributes')


# Terms of Use
USER_REGISTER_TERMS_OF_USE = os.path.join(BASEDIR,
                                          'user_register_terms_of_use.txt')
METADATA_IMPORT_TERMS_OF_USE = os.path.join(BASEDIR,
                                            'metadata_import_terms_of_use.txt')

# Max number of entries the global RSS feed will return
# MAX_FEED_ENTRIES = 10

# Expiration warnings
EXPIRATION_WARNING_TIMEDELTA = datetime.timedelta(days=1)

# Entities pagination
ENTITIES_PER_PAGE = 10

# Federated auth
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

import saml2
PEER_HOST = 'localhost'
PEER_PORT = '8000'
PEER_BASE_URL = 'http://' + PEER_HOST + ':' + PEER_PORT
SAML_CREATE_UNKNOWN_USER = True
SAML_ATTRIBUTE_MAPPING = {
    'mail': ('username', 'mail'),
    'cn': ('first_name', ),
    'sn': ('last_name', ),
    }
SAML_CONFIG = {
    # full path to the xmlsec1 binary programm
    'xmlsec_binary': '/usr/bin/xmlsec1',

    # your entity id, usually your subdomain plus the url to the metadata view
    'entityid': PEER_BASE_URL + '/saml2/metadata/',

    # directory with attribute mapping
    'attribute_map_dir': os.path.join(BASEDIR, 'pysaml2', 'attribute-maps'),

    # this block states what services we provide
    'service': {
        # we are just a lonely SP
        'sp' : {
            'name': 'PEER SP',
            'endpoints': {
                # url and binding to the assetion consumer service view
                # do not change the binding or service name
                'assertion_consumer_service': [
                    (PEER_BASE_URL + '/saml2/acs/', saml2.BINDING_HTTP_POST),
                  ],
                # url and binding to the single logout service view
                # do not change the binding or service name
                'single_logout_service': [
                    (PEER_BASE_URL + '/saml2/ls/', saml2.BINDING_HTTP_REDIRECT),
                    ],
                },

            # attributes that this project need to identify a user
            'required_attributes': ['mail'],

            # attributes that may be useful to have but not required
            'optional_attributes': ['cn', 'sn'],

            # in this section the list of IdPs we talk to are defined
            'idp': {
                # we do not need a WAYF service since there is
                # only an IdP defined here. This IdP should be
                # present in our metadata

                # the keys of this dictionary are entity ids
                'https://localhost/simplesaml/saml2/idp/metadata.php': {
                    'single_sign_on_service': {
                        saml2.BINDING_HTTP_REDIRECT: 'https://localhost/simplesaml/saml2/idp/SSOService.php',
                        },
                    'single_logout_service': {
                        saml2.BINDING_HTTP_REDIRECT: 'https://localhost/simplesaml/saml2/idp/SingleLogoutService.php',
                        },
                    },
                },
            },
        },

    # where the remote metadata is stored
    'metadata': {
        'local': [os.path.join(BASEDIR, 'pysaml2', 'remote_metadata.xml')],
        },

    # set to 1 to output debugging information
    'debug': 1,

    # certificate
    'key_file': os.path.join(BASEDIR, 'pysaml2', 'mycert.key'),  # private part
    'cert_file': os.path.join(BASEDIR, 'pysaml2', 'mycert.pem'),  # public part

    # own metadata settings
    'contact_person': [
        {'given_name': 'Lorenzo',
         'sur_name': 'Gil',
         'company': 'Yaco Sistemas',
         'email_address': 'lgs@yaco.es',
         'contact_type': 'technical'},
        {'given_name': 'Angel',
         'sur_name': 'Fernandez',
         'company': 'Yaco Sistemas',
         'email_address': 'angel@yaco.es',
         'contact_type': 'administrative'},
        ],
    # you can set multilanguage information here
    'organization': {
        'name': [('Yaco Sistemas', 'es'), ('Yaco Systems', 'en')],
        'display_name': [('Yaco', 'es'), ('Yaco', 'en')],
        'url': [('http://www.yaco.es', 'es'), ('http://www.yaco.com', 'en')],
        },
    'valid_for': 24,  # how long is our metadata valid
    }

try:
    from local_settings import *
except ImportError:
    pass
