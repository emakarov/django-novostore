from django.conf.urls.defaults import patterns, include, url
from novostore.urls import *

urlpatterns = patterns('',
    (r'^sale/$', 'blog.views.article', {'artid' : 5 }),
    (r'^design/$', 'blog.views.article', {'artid' : 6 }),
    (r'^installation/$', 'blog.views.article', {'artid' : 7 }),
    (r'^team/$', 'blog.views.article', {'artid' : 10 }),
    (r'^contacts/$', 'blog.views.article', {'artid' : 11 }),
    (r'^objects/$', 'blog.views.blogtermpage', {'termslug' : 'objects' }),
    (r'^faq/$', 'blog.views.blogtermpage', {'termslug' : 'faq' }),
) + urlpatterns