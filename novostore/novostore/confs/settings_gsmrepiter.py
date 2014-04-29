SECRET_KEY = 'mg5-op972k3@qelfbcr#i393q5w4m-dvl9xumt1#)bvf*ey(an'
from novostore.settings import *
# coding=utf-8
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop
#import os
from os import path
import sys

DEBUG = True # False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['gsmrepiter.ru', 'www.gsmrepiter.ru']

TIME_ZONE = 'Europe/Moscow'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'gsmrepiter',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'gsmrepiter',
        'PASSWORD': 'gsmrepiter',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

from south.modelsinspector import add_introspection_rules 

add_introspection_rules([], ["^photologue\.models\.TagField"])
add_introspection_rules([], ["^tagging\.fields\.TagField"])

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    path.join(PROJECT_ROOT,'templates'),
    path.join(PROJECT_ROOT,'templates/gsmrepiter'),
)

ROOT_URLCONF = 'novostore.confs.urls_gsmrepiter'

SUIT_CONFIG = {
    'MENU': (

        # Keep original label and models
        #'sites',
        #'-',

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

#        {'label': _('Common Settings'), 
#        	'models': ('commerce.currency',
#        		   'commerce.currencyexchange',
#          		   'ncatalogue.measureunit',
#        		  ),
#        },
        {'label': _('Blog'), 
        	'models': ('blog.term',
        		   'blog.article',
          		   'sitemanagement.websitemenu',
        		  ),
        },
        {'label': _('Photo'), 
        	'models': ('photologue.gallery',
          		   'photologue.photo',
          		   'photologue.galleryupload',
        		  ),
        },
        {'label': _('Commerce'), 
        	'models': (
        		'shops.shop',
#        		'shops.worker',
#        		'shops.client',
        		'ncatalogue.category',
        		'ncatalogue.product',
        		'shopleads.lead',
#        	 	'commerce.tariff',
#        		'commerce.preorder',
#        		'commerce.deliveryaddress',
#        		'commerce.cart',
#        		'commerce.currency',
#        		'commerce.currencyexchange',
#          		'ncatalogue.measureunit',
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

BLOG_TEMPLATES = (
  ('gsmrepiter/blog/article.html',_("Simple article")),
  ('gsmrepiter/blog/about.html',_("About page")),
  ('blog/contacts.html',_("Contacts")),
)

LEADS_TEMPLATES = {
  'sendrequestform' : 'gsmrepiter/leads/sendrequestlead.html',
  'sendrequestform_footer' : 'gsmrepiter/leads/sendrequestlead_simple.html',
  'sendrequestform_product' : 'gsmrepiter/leads/sendrequestlead_product.html'
}

NCATALOGUE_THEME = lambda r: 'gsmrepiter' #'default'
NCATALOGUE_PRODUCTS_PER_PAGE = 20
INDEX_PAGE_HTML = lambda r: ('gsmrepiter' + '/index.html')
PRODUCT_LIST_HTML = lambda r: ('gsmrepiter' +'/product_list.html')
PRODUCT_PAGE_HTML = lambda r: ('gsmrepiter' +'/product.html')
LOGIN_PAGE_HTML = lambda r: ('gsmrepiter' +'/accounts/login.html')
PROFILE_PAGE_HTML = lambda r: ('gsmrepiter' +'/accounts/profile.html')
SETUP_NEW_PASSWD_PAGE_HTML = lambda r: ('gsmrepiter' +'/accounts/set_up_new_passwd.html')
CART_PAGE_HTML = lambda r: ('gsmrepiter' +'/commerce/cart.html')
CHECKOUT_PAGE_HTML = lambda r: ('gsmrepiter' +'/commerce/checkout.html')
CHECKOUT_CONFIRMED_HTML = lambda r: ('gsmrepiter' + '/commerce/checkout_confirmed.html')
BLOG_INDEX_HTML = lambda r: ('gsmrepiter' + '/blog/index.html')
BLOG_ARTICLELIST_HTML = lambda r: ('gsmrepiter' + '/blog/articlelist.html')
BLOG_ARTICLE_HTML = lambda r: ('gsmrepiter' + '/blog/article.html')

SINGLE_SHOP = True
