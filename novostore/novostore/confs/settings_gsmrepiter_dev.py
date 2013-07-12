SECRET_KEY = 'mg5-op972k3@qelfbcr#i393q5w4m-dvl9xumt1#)bvf*ey(an'
from novostore.settings import *
# coding=utf-8
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop
#import os
from os import path
import sys

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': path.join(ROOT_DIR, 'confs/gsmrepiter'),                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'novostore',
        'PASSWORD': 'novostore',
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
