from django.conf import settings # import the settings file
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop
from django.utils.translation import get_language
from ncatalogue.models import Category, Product
from commerce import models as commerce_models
from django.template import RequestContext

def categories_context(context):
    categories = Category.objects.filter(is_operating = True, shop=context.shop)
    return { 'categories' : categories }

def cart_context(RequestContext):
    #categories = Category.objects.filter(is_operating = True, shop=RequestContext.shop)
    c = None
    cart = None
    if RequestContext.user.is_authenticated():
      try:
        cart = commerce_models.Cart.objects.get(user = RequestContext.user)
      except:
        pass
    else:
      try:
        cart = commerce_models.Cart.objects.get(random_key = RequestContext.session['cartkey'])
      except:
        pass
    cart_elements = commerce_models.CartElement.objects.filter(cart = cart).select_related()
    return { 'cart' : cart, 'cart_elements' : cart_elements, 'len_cart_elements' : len(cart_elements) }
