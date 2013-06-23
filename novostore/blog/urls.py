from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('blog.views',
    (r'article/(?P<artid>\d+)/$', 'article'),
    (r'article/(?P<artid>\d+)$', 'article'),
    (r'search/$', 'search'),
    (r't/(?P<termslug>\w+)$', 'blogtermpage'),
    (r't/(?P<termslug>\w+)/$', 'blogtermpage'),
    (r'' , 'index'),
)