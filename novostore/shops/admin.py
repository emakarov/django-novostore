# coding=utf-8

""" Admin configuration for shops

"""

from django.contrib import admin
from django.contrib import messages

from django.forms.widgets import HiddenInput
from django.db.models import Q, F

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop
from suit.admin import SortableModelAdmin
from mptt.admin import MPTTModelAdmin
from commerce import models as commerce_models
from shops import models as shop_models
from mptt.forms import TreeNodeChoiceField 
from django import forms
from utils.visibility import VisibleAdmin

class ShopAdmin(VisibleAdmin):
  list_display = ['name','domain','owner','theme']

class ClientAdmin(VisibleAdmin):
  list_display = ['user','shop']

class WorkerAdmin(VisibleAdmin):
  list_display = ['user','shop']


admin.site.register(shop_models.Shop, ShopAdmin)
admin.site.register(shop_models.Client, ClientAdmin)
admin.site.register(shop_models.Worker, WorkerAdmin)

