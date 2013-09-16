# coding=utf-8
from django.shortcuts import render_to_response, redirect
from django.template import Template,RequestContext, loader, Context
from django.conf import settings
from django.contrib.auth.decorators import login_required
from photologue.models import Photo
from django.http import HttpResponse
# Create your views here.
from datetime import tzinfo, timedelta, datetime
from django.views.decorators.cache import never_cache
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.translation import ugettext_noop
from django.utils.translation import get_language
from ncatalogue import models as ncatalogue_models
from django.db.models import Q,F
from shops import models as shop_models

PPP = settings.NCATALOGUE_PRODUCTS_PER_PAGE
index_page_html = settings.INDEX_PAGE_HTML
product_page_html = settings.PRODUCT_PAGE_HTML
product_list_html = settings.PRODUCT_LIST_HTML

def index(request):
#  print request.session.session_key
#  print request.shop
#  try:
#    print request.session['has_commented']
#  except:
#    print "no"
#  request.session['has_commented'] = 'fffff'
  #print request.session['has_commented']
  categories_all = ncatalogue_models.Category.objects.filter(is_operating = True, shop=request.shop)
  try:
    products = ncatalogue_models.Product.objects.filter(
  	  Q(categories = categories_all[0]) | Q(categories__parent=categories_all[0])
  	).distinct()[0:4]
  except:
    products = None
  params = {  
  	'products' : products,
  	'show_breadcrumb' : False,
  }
  return render_to_response(index_page_html(request), params, context_instance = RequestContext(request))

def category_list(request,category_slug):
  category = ncatalogue_models.Category.objects.get(slug = category_slug)
  products = ncatalogue_models.Product.objects.filter(
  	  Q(categories = category) | Q(categories__parent=category)
  	).distinct()
  catfilter = category.filtergroups.all()[0]
  #print catfilter.items.all()[0].name
  ids = request.GET.get('ids', None)
  price_from = request.GET.get('price_from', None)
  price_to = request.GET.get('price_to', None)
  q = request.GET.get('q', None)
  if ids:
    ids = ids.replace('+', ' ').split(' ')
    for i in ids:
      cat = ncatalogue_models.Category.objects.get(id=int(i))
      products = products.filter(categories=cat)
  if price_from:
    products = products.filter(price__gte=price_from)
  if price_to:
    products = products.filter(price__lte=price_to)
  if q:
    products = products.filter(
                   Q(name__icontains=q) | 
                   Q(description__icontains=q) |
                   Q(long_description__icontains=q) |
                   Q(text__icontains=q)
             )
  params = {  
  	'products' : products,
  	'show_breadcrumb' : True,
  	'category' : category,
  	'catfilter' : catfilter,
  	'ids' : ids,
  	'price_from' : price_from,
  	'price_to' : price_to,
  	'q' : q
  }
  return render_to_response(product_list_html(request), params, context_instance = RequestContext(request))


def productpage(request,product_id):
  categories = ncatalogue_models.Category.objects.filter(is_operating = True)
  product = ncatalogue_models.Product.objects.get(id = product_id)
  try:
    child_category = product.categories.filter(is_operating = True).exclude(parent=None)[0]
  except:
    child_category = product.categories.filter(is_operating = True)[0]
  might_like_products = ncatalogue_models.Product.objects.filter(
  	  Q(categories = categories[0]) | Q(categories__parent=categories[0])
  	).exclude(id=product_id).distinct().order_by('?')[0:4]
  params = {  
  	'product' : product,
  	'child_category' : child_category,
  	'might_like_products' : might_like_products,
  	'show_breadcrumb' : True
  }
  return render_to_response(product_page_html(request), params, context_instance = RequestContext(request))
  
def simpleproductsearch(request):
  q = request.REQUEST.get('q',None)
  if q:
    products = ncatalogue_models.Product.objects.filter(
                                              Q(upc__icontains=q) |
                                              Q(name__icontains=q) |
                                              Q(description__icontains=q) |
                                              Q(long_description__icontains=q)
                                              )
  else:
    products = ncatalogue_models.Product.objects.none()
  params = {  
  	'products' : products,
  	'show_breadcrumb' : True,
  	'category' : None,
  	'searchstring' : q
  }
  return render_to_response(product_list_html(request), params, context_instance = RequestContext(request))
