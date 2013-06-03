# coding=utf-8
from django.shortcuts import render_to_response
from django.template import Context, RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.utils import simplejson
from django.conf import settings
import forms as account_forms
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.utils.translation import ugettext_lazy as _
from captcha.fields import CaptchaField
from accounts.models import AccountsUser as User
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
from commerce.views import get_cart, get_or_create_cart_by_user, combine_carts, get_cart_by_request_cartkey
from commerce import forms as commerce_forms
from commerce import models as commerce_models
from utils.stuff import deserialize_form

login_page_html = settings.LOGIN_PAGE_HTML
setup_new_passwd = settings.SETUP_NEW_PASSWD_PAGE_HTML
profile_page = settings.PROFILE_PAGE_HTML

def saveprofileajax(request):
    form = request.REQUEST.get('form')
    #print deserialize_form(form)
    try:
      formtag = request.REQUEST.get('formtag')
      user = request.user
      if user.is_authenticated():
        if formtag == 'account_form':
          formname_form = account_forms.AccountsUserFormShort(deserialize_form(form),instance=user)
        elif formtag == 'delivery_form' :
          formname_form = commerce_forms.DeliveryAddressForm(deserialize_form(form),instance=user.delivery_addresses.all()[0])
        formname_form.save()
        jsondumps =  json.dumps({'status': 'saved', 'formtag' : formtag})
      else:
        jsondumps = json.dumps({'status' : 'notautorized', 'formtag' : formtag})
    except:
      jsondumps = json.dumps({'status' : 'error', 'formtag' : formtag})
    return HttpResponse(jsondumps, content_type="application/json")


def profile(request):
    account_form = account_forms.AccountsUserFormShort(instance=request.user)
    try:
      da = commerce_models.DeliveryAddress.objects.get(user=request.user)
    except:
      da = commerce_models.DeliveryAddress()
      da.user = user
      da.save()
    delivery_form = commerce_forms.DeliveryAddressForm(instance = da)
    preorders = commerce_models.PreOrder.objects.filter(shopoholic = request.user)
    params = { 'account_form' : account_form, 
    		'delivery_form' : delivery_form,
    		'preorders' : preorders, 
    		'added_word' : _("My profile") }
    return render_to_response(profile_page(request), params , context_instance = RequestContext(request))


def email_for_restorepassword(request):
  if request.method == "POST":    
    email_recover = request.REQUEST.get("email_restore")
    user = None
    try:
      user = User.objects.get(email = email_recover)
    except:
      pass
    print user
    if user:
      user.confirm_key = randomconfirmationlink()
      user.save()
      plain_mail = loader.get_template('mail_restore.txt')
      c = Context({'up': user, 'request' : request})
      subj = _("Password Restore")
      e_s = settings.EMAIL_SERVER_ADRESS_NOREPLY
      message = plain_mail.render(c)
      if settings.DEBUG:
        print message
        print user.email
      else:
        mail.send_mail(subj, message, e_s, [ user.email ])
    return render_to_response('email_send.html', {} ,  context_instance = RequestContext(request))
  else:
    confirm_key = request.REQUEST.get("confirm_key")
    user = None
    user = User.objects.get(confirm_key = confirm_key)
    user.backend='django.contrib.auth.backends.ModelBackend'
    auth.login(request, user)
    return render_to_response(setup_new_passwd(request), {'phase' : 'input' } ,  context_instance = RequestContext(request))

def change_password(request):
  password = request.REQUEST.get("password",None)
  try:
    cart = get_cart_by_request_cartkey(request)
  except:
    return redirect('/')
  try:
    nextp = request.session['nextp']
  except:
    nextp = '/'
  user = request.user  
  if user is not None:
    cart2 = get_or_create_cart_by_user(user)
    combine_carts(cart,cart2)
  if password and len(password)>1:
    u = request.user
    u.set_password(password)
    u.save()
    if nextp != '/':
      return redirect(nextp)
    return render_to_response(setup_new_passwd(request), {'phase' : 'ok' } ,  context_instance = RequestContext(request))
  else: 
    return render_to_response(setup_new_passwd(request), {'phase' : 'badpasswd' } ,  context_instance = RequestContext(request))

def change_password_by_new_social_user(request):
  password = request.REQUEST.get("password",None)
  cart = None
  try:
    cart = get_cart_by_request_cartkey(request)
  except:
    pass
  try:
    nextp = request.session['nextp']
  except:
    nextp = '/'
  user = request.user  
  if user is not None and cart is not None:
    cart2 = get_or_create_cart_by_user(user)
    combine_carts(cart,cart2)
  if password and len(password)>1:
    u = request.user
    u.set_password(password)
    u.save()
    return render_to_response(setup_new_passwd(request), {'phase' : 'ok', 'social' : True, 'nextp' : nextp } ,  context_instance = RequestContext(request))
  else: 
    return render_to_response(setup_new_passwd(request), {'phase' : 'badpasswd', 'social' : True, 'nextp' : nextp } ,  context_instance = RequestContext(request))
    

def combinecarts(request):
  try:
    cart = get_cart_by_request_cartkey(request)
  except:
    return redirect('/')
  try:
    nextp = request.session['nextp']
  except:
    nextp = '/'
  user = request.user  
  if user is not None:
    cart2 = get_or_create_cart_by_user(user)
    combine_carts(cart,cart2)
  return redirect(nextp)

def login(request):
    if request.method == "POST":
        #username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        nextp = request.POST.get('next',None)
        #print nextp
        username = None
        user = None
        cart = get_cart(request)
        if not nextp:
          nextp = '/'
        try:
	  username = User.objects.get(email = email).username
	except:
	  pass
	if not username:
	  try:
	    username = User.objects.get(username = email).username
	  except:
	    pass
	if username:
          user = auth.authenticate(username=username, password=password)
        if user is not None:
            cart2 = get_or_create_cart_by_user(user)
            combine_carts(cart,cart2)
            if user.is_active:
                auth.login(request, user)
                return redirect(nextp)
                # Redirect to a success page.
            else:
                return redirect(nextp)
                #pass
                # Return a 'disabled account' error message
        else:
            return redirect('/accounts/login/?next='+nextp)
            #pass
            # Return an 'invalid login' error message.
    else:
        nextp = request.REQUEST.get('next',None)
        form = account_forms.HRUserCreationForm()
        if request.user.is_authenticated() :
            return redirect('/')
        if nextp:
	  params = {'next' : nextp , 'form' : form, 'mode' : 'login'}
	else:
	  params = {'next' : '/' , 'form' : form , 'mode' : 'login'}
        return  (render_to_response(login_page_html(request),
        params,  
        context_instance = RequestContext(request)))

def register(request):
    if request.method == "POST":
        form = account_forms.HRUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                if user.is_active:
                    user.backend='django.contrib.auth.backends.ModelBackend'
                    auth.login(request, user)
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['first_name']
                    rcl = randomconfirmationlink()
                    #up = UserProfile.objects.get(user = user)
                    user.confirm_key = rcl
                    user.save()
                    plain_mail = loader.get_template('mail_confirmation.txt')
                    c = Context({'rcl': rcl})
                    subj = settings.REGISTER_TEXT_SUBJECT
                    e_s = settings.EMAIL_SERVER_ADRESS_NOREPLY
                    c = Context({'rcl': rcl})
                    message = plain_mail.render(c)
                    if settings.DEBUG:
                      print message, user.email
                    else:
                      mail.send_mail(subj, message, e_s, [ user.email ])
#                    SendMail.delay(subj, plain_mail.render(c), es, [ registered_user.email ])
                    return redirect('/')
                    # Redirect to a success page.
                else:
                    return redirect('/')
                    # Return a 'disabled account' error message
            else:
                return redirect('/')
        else:
            return render_to_response(login_page_html(request), {'form': form, 'mode' : 'register' } ,  context_instance = RequestContext(request))
            #return redirect('/')
            # Return an 'invalid login' error message.
    else:
        form = account_forms.HRUserCreationForm()
        return render_to_response(login_page_html(request), {'form': form, 'mode' : 'register' } ,  context_instance = RequestContext(request))

def logout(request):
    auth.logout(request)
    return redirect('/')

#FORMS

def randomconfirmationlink():
	digits = "".join( [random.choice(string.digits) for i in xrange(10)] )
	chars = "".join( [random.choice(string.letters) for i in xrange(10)] ).lower()
	digits2 = "".join( [random.choice(string.digits) for i in xrange(10)] )
	return digits+chars+digits2

