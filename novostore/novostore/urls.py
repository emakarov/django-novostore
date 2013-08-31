from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from ncatalogue import urls as ncat_urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'novostore.views.home', name='home'),
    # url(r'^novostore/', include('novostore.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^commerce/', include('commerce.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^articles/', include('blog.urls')),
    url(r'', include('social_auth.urls')),
    (r'^$', 'ncatalogue.views.index'),
    (r'psearch/$', 'ncatalogue.views.simpleproductsearch'),
) 

urlpatterns += patterns('django.contrib.staticfiles.views',
        (r'^favicon.ico', 'serve', {'path' : 'favicon.png'}),
        url(r'^static/(?P<path>.*)$', 'serve'),
        url(r'^ru/static/(?P<path>.*)$', 'serve'),
        url(r'^media/(?P<path>.*)$', 'serve'),
        )
        
        
        
urlpatterns += ncat_urls.urlpatterns
