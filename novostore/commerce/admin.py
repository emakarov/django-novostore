# coding=utf-8

""" Admin configuration for ncatalogue

"""
#from util.treetabularinline import TabularLinkInline
#from util import base_admin as util_admin

from django.contrib import admin
from django.contrib import messages

from django.forms.widgets import HiddenInput
from django.db.models import Q, F

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop
from suit.admin import SortableModelAdmin
from mptt.admin import MPTTModelAdmin
from commerce.models import *
from mptt.forms import TreeNodeChoiceField 
from django import forms
from utils.visibility import VisibleAdmin, VisibilityTabularInline

class CartElementInlineAdmin(VisibilityTabularInline):
  model = CartElement
  readonly_fields  = ['product','quantity']

class PreOrderElementInlineAdmin(VisibilityTabularInline):
  model = PreOrderElement
  readonly_fields  = ['product','price','quantity','sum']

class CurrencyAdmin(admin.ModelAdmin):
  list_display = ['name']

class TariffAdmin(admin.ModelAdmin):
  list_display = ['name']

class CurrencyExchangeAdmin(admin.ModelAdmin):
  list_display = ['from_currency','to_currency','course']

class CartAdmin(VisibleAdmin):
  list_display = ['created_at','is_active','user','modified_at']
  inlines = [CartElementInlineAdmin,]

class PreOrderAdmin(VisibleAdmin):
  list_display = ['shopoholic','id','price','paid','created_at','is_active','modified_at']
  inlines = [PreOrderElementInlineAdmin,]
  search_fields = ['shopoholic__username','id','paid','created_at','is_active','modified_at']


class DeliveryAddressAdmin(admin.ModelAdmin):
  list_display = ['city','street_house','user','phone']


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Tariff, TariffAdmin)
admin.site.register(PreOrder, PreOrderAdmin)
admin.site.register(CurrencyExchange, CurrencyExchangeAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(DeliveryAddress,DeliveryAddressAdmin)