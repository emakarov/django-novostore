# coding=utf-8

# Django settings for olympics project.
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop
#import os
from os import path
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

ROOT_DIR = path.abspath(path.dirname(path.abspath(__file__)))
PROJECT_ROOT = ROOT_DIR
PROJECT_DIR = path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': path.join(ROOT_DIR, 'novostore'),                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'novostore',
        'PASSWORD': 'novostore',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru'

LANGUAGES = (
#        ('en', _('English')),
        ('ru', _('Russian')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''
MEDIA_ROOT = path.join(ROOT_DIR, 'static/')
ADMIN_MEDIA_ROOT = path.join(ROOT_DIR, 'static/admin/')
ADMIN_MEDIA_PREFIX = '/static/admin/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''
MEDIA_URL = '/media/'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
#STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
#STATIC_URL = '/static/'

STATIC_ROOT = STATICFILES_ROOT = path.join(ROOT_DIR,'static')

STATIC_URL = STATICFILES_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'mg5-op972k3@qelfbcr#i393q5w4m-dvl9xumt1#)bvf*ey(an'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'shops.shopdetectionmiddleware.ShopDetectionMiddleware',
)

ROOT_URLCONF = 'novostore.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'novostore.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    path.join(PROJECT_ROOT,'templates'),
)

LOCALE_PATHS = (
  path.join(PROJECT_ROOT,'locale'),
)
#print LOCALE_PATHS

INSTALLED_APPS = (
    'suit',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.webdesign',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'south',
    'photologue',
    'django_extensions',
    'mptt',
    'accounts',
    'commerce',
    'ncatalogue',
    'shops',
    'social_auth',
    #'tagging',
    'utils',
    'django.contrib.comments',
    'sitemanagement',
    'blog',
    'shopleads',
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


TWEET_STORAGE = path.join(ROOT_DIR, 'tweet_storage/')

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'ncatalogue.context_processors.categories_context',
    'commerce.context_processors.cart_context',
    'sitemanagement.context_processors.menu_context',
)


SUIT_CONFIG = {
    'MENU': (

        # Keep original label and models
        'sites',
        '-',

        # Rename app and set icon
        #{'app': 'accounts', 'label': 'Users', 'icon':'icon-user'},
        #{'app': 'auth', 'label': 'Groups', 'icon':'icon-user'},

        {'label': _('Users'), 'icon':'icon-user', 'models': (
            'accounts.accountsuser','auth.group', 
        )},


        # Reorder app models
        #{'app': 'auth', 'models': ('user', 'group')},

        # Custom app, with models
        #{'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
        
        #{'label' : _('Shops'), 'app' : 'shops' },

        {'label': _('Common Settings'), 
        	'models': ('commerce.currency',
        		   'commerce.currencyexchange',
          		   'ncatalogue.measureunit',
        		  ),
        },

        {'label': _('Commerce'), 
        	'models': (
        		'shops.shop',
        		'shops.worker',
        		'shops.client',
        		'ncatalogue.category',
        		'ncatalogue.product',
        	 	'commerce.tariff',
        		'commerce.preorder',
        		'commerce.deliveryaddress',
        		'commerce.cart',
        		),
        	'icon' : 'icon-shopping-cart'
        },


        # Cross-linked models with custom name; Hide default icon
        #{'label': 'Custom', 'icon':None, 'models': (
        #    'auth.group',
        #    {'model': 'auth.user', 'label': 'Staff'}
        #)},

        # Custom app, no models (child links)
        #{'label': 'Users', 'url': 'auth.user', 'icon':'icon-user'},

        # Separator
        '-',

        # Custom app and model with permissions
        #{'label': 'Secure', 'permissions': 'auth.add_user', 'models': [
        #    {'label': 'custom-child', 'permissions': ('auth.add_user', 'auth.add_group')}
        #]},
    )
}

PHOTOLOGUE_MAXBLOCK = 1024*2**10

NCATALOGUE_THEME = lambda r: r.shop.theme #'default'
NCATALOGUE_PRODUCTS_PER_PAGE = 20
INDEX_PAGE_HTML = lambda r: (r.shop.theme + '/index.html')
PRODUCT_LIST_HTML = lambda r: (r.shop.theme +'/product_list.html')
PRODUCT_PAGE_HTML = lambda r: (r.shop.theme +'/product.html')
LOGIN_PAGE_HTML = lambda r: (r.shop.theme +'/accounts/login.html')
PROFILE_PAGE_HTML = lambda r: (r.shop.theme +'/accounts/profile.html')
SETUP_NEW_PASSWD_PAGE_HTML = lambda r: (r.shop.theme +'/accounts/set_up_new_passwd.html')
CART_PAGE_HTML = lambda r: (r.shop.theme +'/commerce/cart.html')
CHECKOUT_PAGE_HTML = lambda r: (r.shop.theme +'/commerce/checkout.html')
CHECKOUT_CONFIRMED_HTML = lambda r: (r.shop.theme + '/commerce/checkout_confirmed.html')
BLOG_INDEX_HTML = lambda r: (r.shop.theme + '/blog/index.html')
BLOG_ARTICLELIST_HTML = lambda r: (r.shop.theme + '/blog/articlelist.html')
BLOG_ARTICLE_HTML = lambda r: (r.shop.theme + '/blog/article.html')

REGISTER_TEXT_SUBJECT = _("Register on e-commerce shop")
EMAIL_SERVER_ADRESS_NOREPLY = "info@drivepixels.ru"

#from south.modelsinspector import add_introspection_rules 

#add_introspection_rules([], ["^photologue\.models\.TagField"])
#add_introspection_rules([], ["^tagging\.fields\.TagField"])

AUTH_USER_MODEL = 'accounts.AccountsUser'

#====OPEN AUTH SETTINGS=====#
AUTHENTICATION_BACKENDS = (
#    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
#    'social_auth.backends.google.GoogleOAuthBackend',
#    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
#    'social_auth.backends.yahoo.YahooBackend',
##    'social_auth.backends.browserid.BrowserIDBackend',
#    'social_auth.backends.contrib.linkedin.LinkedinBackend',
#    'social_auth.backends.contrib.disqus.DisqusBackend',
#    'social_auth.backends.contrib.livejournal.LiveJournalBackend',
#    'social_auth.backends.contrib.orkut.OrkutBackend',
#    'social_auth.backends.contrib.foursquare.FoursquareBackend',
#    'social_auth.backends.contrib.github.GithubBackend',
#    'social_auth.backends.contrib.vk.VKOAuth2Backend',
#    'social_auth.backends.contrib.live.LiveBackend',
#    'social_auth.backends.contrib.skyrock.SkyrockBackend',
#    'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
#    'social_auth.backends.contrib.readability.ReadabilityBackend',
#    'social_auth.backends.contrib.fedora.FedoraBackend',
#    'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)
TWITTER_CONSUMER_KEY         = ''
TWITTER_CONSUMER_SECRET      = ''

##FACEBOOK TO BE REDONE##
FACEBOOK_APP_ID = '382245681888119'
FACEBOOK_API_SECRET = '4e6db570c3127b66dbba5939b8b2e4a6'
FACEBOOK_EXTENDED_PERMISSIONS = ['email']
##==##

LINKEDIN_CONSUMER_KEY        = ''
LINKEDIN_CONSUMER_SECRET     = ''
ORKUT_CONSUMER_KEY           = ''
ORKUT_CONSUMER_SECRET        = ''
GOOGLE_CONSUMER_KEY          = ''
GOOGLE_CONSUMER_SECRET       = ''
GOOGLE_OAUTH2_CLIENT_ID      = ''
GOOGLE_OAUTH2_CLIENT_SECRET  = ''
FOURSQUARE_CONSUMER_KEY      = ''
FOURSQUARE_CONSUMER_SECRET   = ''
VK_APP_ID                    = ''
VK_API_SECRET                = ''
LIVE_CLIENT_ID               = ''
LIVE_CLIENT_SECRET           = ''
SKYROCK_CONSUMER_KEY         = ''
SKYROCK_CONSUMER_SECRET      = ''
YAHOO_CONSUMER_KEY           = ''
YAHOO_CONSUMER_SECRET        = ''
READABILITY_CONSUMER_SECRET  = ''
READABILITY_CONSUMER_SECRET  = ''

LOGIN_URL          = '/accounts/login-form/'
LOGIN_REDIRECT_URL = '/accounts/logged-in/'
LOGIN_ERROR_URL    = '/accounts/login-error/'

#SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/accounts/another-login-url/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/accounts/combinecarts/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/accounts/new-users-redirect-url/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/accounts/new-association-redirect-url/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/accounts/account-disconnected-redirect-url/'
SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'
#===END OF SOCIAL AUTH SETTINGS=======#
