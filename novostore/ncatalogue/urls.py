from django.conf.urls import patterns, include, url

urlpatterns = patterns('ncatalogue.views',
    (r'product/(?P<product_id>\d+)/$', 'productpage'),
    (r'^(?P<category_slug>.+)/$', 'category_list'),
)