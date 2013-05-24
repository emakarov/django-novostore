# coding=utf-8
from django.shortcuts import render_to_response
from django.template import Context, RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.utils import simplejson
from django.conf import settings
from django import forms
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.utils.translation import ugettext_lazy as _
from captcha.fields import CaptchaField
from accounts.models import AbstractBaseUser as User
from commerce import models as commerce_models
from ncatalogue import models as ncat_models
from datetime import date
from django.conf import settings
import logging
import random
import string
import md5
import base64
from django.shortcuts import redirect
import json
import hmac
import hashlib
from django.core import mail
from utils.stuff import codegenerator
from commerce import forms as commerce_forms


def addtocart(request):
  if request.method == "POST":    
    product_id = int(request.REQUEST.get("product_id"))
    productquantity = int(request.REQUEST.get("productquantity"))
    user = request.user
    cart = None
    c = None
    product = ncat_models.Product.objects.get(id=product_id)
    cart = get_cart(request)
    #print product
    try:
      c = cart.elements.filter(product = product)[0]
    except:
      pass
    if c:
      c.quantity = c.quantity + productquantity
      c.save()
    else:
      c = commerce_models.CartElement()
      c.product = product
      c.quantity = productquantity
      c.cart = cart
      c.save()
    request.session['cartkey'] = cart.random_key
    return HttpResponse(json.dumps({'cart': cart.number_of_items()['quantity__sum'] }), content_type="application/json")
  else:
    return HttpResponse(json.dumps({'ajax_status': 'error'}), content_type="application/json")

def deletefromcart(request):
  if request.method == "POST":    
    cart = get_cart(request)
    if cart:
      try:
        element_id = int(request.REQUEST.get("element_id"))
        elem = cart.elements.get(id = element_id)
        elem.delete()
        q = cart.number_of_items()['quantity__sum']
        return HttpResponse(json.dumps({
        	                        'cartitems': q if q else 0,
                                        'ajax_status' : 'deleted'
                                       }
                           ),content_type="application/json")
      except:
        return HttpResponse(json.dumps({'ajax_status': 'error'}), content_type="application/json")
  else:
    return HttpResponse(json.dumps({'ajax_status': 'error'}), content_type="application/json")

def changeelementincart(request):
  if request.method == "POST":    
    cart = get_cart(request)
    if cart:
      #try:
        element_id = int(request.REQUEST.get("element_id"))
        modify = request.REQUEST.get("modify")
        elem = cart.elements.get(id = element_id)
        status = None
        if modify == 'increase':
          elem.quantity += 1
          status = 'increased'
        if modify == 'decrease':
          elem.quantity -= 1
          status = 'decreased'
        elem.save()
        if elem.quantity == 0:
          elem.delete()
          status = 'deleted'
        return HttpResponse(json.dumps({
        	                        'element_id': element_id,
                                        'quantity' : elem.quantity,
                                        'ajax_status' : status
                                       }
                           ),content_type="application/json")
      #except:
      #  return HttpResponse(json.dumps({'ajax_status': 'error'}), content_type="application/json")
  else:
    return HttpResponse(json.dumps({'ajax_status': 'error'}), content_type="application/json")
  

def cart(request):
    added_word = _("My cart")
    params = { 'added_word' : added_word }
    return render_to_response(settings.CART_PAGE_HTML, params ,  context_instance = RequestContext(request))

def checkout(request):
    if not request.user.is_authenticated():
      return redirect('/accounts/login/?next=/commerce/checkout/')
    added_word = _("Checkout")
    delivery_addresses = commerce_models.DeliveryAddress.objects.filter(user=request.user)
    delivery_address_count = len(delivery_addresses)
    #print delivery_address_count
    if delivery_address_count == 0 :
      delivery_address = commerce_models.DeliveryAddress()
      delivery_address.user = request.user
      delivery_address.save()
    else:
      delivery_address = delivery_addresses[0]
    #delivery_addresses = commerce_models.DeliveryAddress.objects.filter(user=request.user)
    form = commerce_forms.DeliveryAddressForm(instance=delivery_address)
    form.fields['user'].widget = forms.HiddenInput()
    #print delivery_address
    params = { 'added_word' : added_word , 
    		#'delivery_addresses' : delivery_addresses, 
    		'delivery_address_count' : delivery_address_count,
    		'form' : form
    	     }
    return render_to_response(settings.CHECKOUT_PAGE_HTML, params ,  context_instance = RequestContext(request))
    
def checkout_confirm_address(request):
    if request.method == 'POST':
      form = commerce_forms.DeliveryAddressForm(request.POST)
      try:
        delivery_address = commerce_models.DeliveryAddress.objects.get(user=request.user)
      except:
        delivery_address = commerce_models.DeliveryAddress()
      if form.is_valid():
        city = form.cleaned_data['city']
        street_house = form.cleaned_data['street_house']
        zipcode = form.cleaned_data['zipcode']
        #lat = form.cleaned_data['lat']
        #lon = form.cleaned_data['lon']
        user = request.user
        delivery_address.city = city
        delivery_address.street_house = street_house
        delivery_address.zipcode = zipcode
        #delivery_address.lat = lat
        #delivery_address.lon = lon
        delivery_address.user = user
        delivery_address.save()
        cart = get_cart(request)
        copy_cart_to_order(cart,user)
      params = {}
      return render_to_response(settings.CHECKOUT_CONFIRMED_HTML, params ,  context_instance = RequestContext(request))

def get_cart(request):
    user=request.user
    try:
      return get_or_create_cart_by_user(user,request.session['cartkey'])
    except:
      return get_or_create_cart_by_user(user)

def copy_cart_to_order(cart,user):
    preorder = commerce_models.PreOrder()
    preorder.paid = False
    preorder.shopoholic = user
    preorder.requested_for_delivery = True
    preorder.payment_on_delivery = True
    preorder.is_active = True
    preorder.save()
    for el in cart.elements.all():
      print "ADDING"
      pol = commerce_models.PreOrderElement()
      pol.product = el.product
      pol.quantity = el.quantity
      pol.preorder = preorder
      pol.save()
    return 0
    

def get_or_create_cart_by_user(user,cartkey=None):
    cart = None
    if user.is_authenticated():
      try:
        cart = commerce_models.Cart.objects.get(user = user)
      except:
        pass
    else:
      try:
        cart = commerce_models.Cart.objects.get(random_key = cartkey)
      except:
        pass
    if not cart:
      cart = commerce_models.Cart()
      cartkey = codegenerator(10,10,10)
      cart.random_key = cartkey
      if user.is_authenticated():
        cart.user = user
      cart.save()
    return cart

def combine_carts(c1,c2):
  #c2 is for authenticated user, c1 is for user=AnoninousUser
  print c1
  print c2
  for el in c1.elements.all():
    el.cart = c2
    el.save()
  return 0
    
  
