# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.conf import settings
from django.forms import widgets
from django.forms.extras.widgets import SelectDateWidget
#from honeyroiboos.blog.custom_widget import TinyMCE
from django.shortcuts import render_to_response
#from ncatalogue import models as ncat_models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop
from django.db.models import Sum
from django.core.validators import *
from django.db.models import Q,F
from utils.visibility import VisibleManager, SuperUserVisibleManager

class Shop(models.Model):
  name = models.CharField(_("Name"),max_length=50)
  domain = models.CharField(_("Domain"),max_length=255)
  owner = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="shops")
  theme = models.CharField(_("Theme of website"),max_length=50)

  objects = SuperUserVisibleManager(Q(owner=lambda r:r.user))
  
  def __unicode__(self):
    return "%s"%(self.name)
  
  class Meta:
    verbose_name = _("Shop")
    verbose_name_plural = _("Shops")
    
class Worker(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="worked")
  shop = models.ForeignKey(Shop,related_name="workers")

  objects = VisibleManager(Q(user=lambda r:r.user) | Q(shop__workers__user=lambda r:r.user) )
  
  def __unicode__(self):
    return "%s %s"%(self.user.username,self.shop.name)
  
  class Meta:
    verbose_name = _("Worker")
    verbose_name_plural = _("Workers")

class Client(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="clients")
  shop = models.ForeignKey(Shop,related_name="clients")

  objects = VisibleManager(Q(user=lambda r:r.user)) # | Q(shop=lambda r:r.user.clients) )
  
  def __unicode__(self):
    return "%s %s"%(self.name)
  
  class Meta:
    verbose_name = _("Client")
    verbose_name_plural = _("Clients")
  
  