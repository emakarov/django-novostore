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
from commerce.views import get_cart, get_or_create_cart_by_user, combine_carts

login_page_html = settings.LOGIN_PAGE_HTML
setup_new_passwd = settings.SETUP_NEW_PASSWD_PAGE_HTML

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
    return render_to_response(setup_new_passwd, {'phase' : 'input' } ,  context_instance = RequestContext(request))

def change_password(request):
  password = request.REQUEST.get("password",None)
  if password and len(password)>1:
    u = request.user
    u.set_password(password)
    u.save()
    return render_to_response(setup_new_passwd, {'phase' : 'ok' } ,  context_instance = RequestContext(request))
  else: 
    return render_to_response(setup_new_passwd, {'phase' : 'badpasswd' } ,  context_instance = RequestContext(request))
    
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
        form = HRUserCreationForm()
        if request.user.is_authenticated() :
            return redirect('/')
        if nextp:
	  params = {'next' : nextp , 'form' : form, 'mode' : 'login'}
	else:
	  params = {'next' : '/' , 'form' : form , 'mode' : 'login'}
        return  (render_to_response(login_page_html,
        params,  
        context_instance = RequestContext(request)))

def register(request):
    if request.method == "POST":
        form = HRUserCreationForm(request.POST)
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
            return render_to_response(login_page_html, {'form': form, 'mode' : 'register' } ,  context_instance = RequestContext(request))
            #return redirect('/')
            # Return an 'invalid login' error message.
    else:
        form = HRUserCreationForm()
        return render_to_response(login_page_html, {'form': form, 'mode' : 'register' } ,  context_instance = RequestContext(request))

def logout(request):
    auth.logout(request)
    return redirect('/')

#FORMS
class HRUserCreationForm(auth.forms.UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    #captcha = CaptchaField()

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email__exact = email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(_("User with this email already exists"))

    class Meta:
        model = User
        fields = ('username', 'email')

class LoginForm(forms.Form):
    email_or_login = forms.CharField(max_length=100)
    password = forms.CharField()

    def clean_email_or_login(self):
        email_or_login = self.cleaned_data['email_or_login']
        password = self.cleaned_data['password']
        try:
            user = User.objects.get(email__exact = email_or_login, password = password)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(_("User with this credentials not found"))

def randomconfirmationlink():
	digits = "".join( [random.choice(string.digits) for i in xrange(10)] )
	chars = "".join( [random.choice(string.letters) for i in xrange(10)] ).lower()
	digits2 = "".join( [random.choice(string.digits) for i in xrange(10)] )
	return digits+chars+digits2

