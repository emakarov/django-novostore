from django.conf.urls.defaults import patterns, include, url
from novostore.urls import *

urlpatterns = patterns('',
    (r'^faq/$', 'blog.views.article', {'artid' : 3 }),
) + urlpatterns