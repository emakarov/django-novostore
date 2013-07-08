from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('blog.views',
    (r'article/(?P<artid>\d+)/$', 'article'),
    (r'redactorimagejson/$', 'redactorimagejson'),
    (r'search/$', 'search'),
    (r't/(?P<termslug>\w+)$', 'blogtermpage'),
    (r't/(?P<termslug>\w+)/$', 'blogtermpage'),
    (r'' , 'index'),
)