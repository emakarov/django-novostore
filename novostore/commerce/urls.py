from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('commerce.views',
    (r'addtocart/','addtocart'),
    (r'deletefromcart/','deletefromcart'),
    (r'changeelementincarturl/','changeelementincart'),
    (r'cart/','cart'),
    (r'checkout/','checkout'),
    (r'checkout_confirm_address/','checkout_confirm_address'),
)