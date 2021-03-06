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
from ncatalogue.models import *
from commerce.models import *
from mptt.forms import TreeNodeChoiceField 
from django import forms
from utils.visibility import VisibleAdmin

import copy

def cloneobj(obj):
  dup = copy.copy(obj)
  dup.id = None
  dup.pk = None
  dup.save()
  return dup

def duplicate_product(modeladmin, request, queryset):
  for obj in queryset:
    p = cloneobj(obj)
    for a in obj.details.all():
      b = cloneobj(a)
      p.details.add(b)
    for c in obj.categories.all():
      p.categories.add(c)
    p.name = p.name+' (COPY)'
    p.gallery = None
    p.cover = None
    p.save()

duplicate_product.short_description = "Copy this item (duplicate)"

class TreeModelInlineForm(forms.ModelForm): 
  tree_field = TreeNodeChoiceField(queryset=Category.objects.all())

#class CurrencyAdmin(admin.ModelAdmin):
#  list_display = ['name']

class MeasureUnitAdmin(admin.ModelAdmin):
  list_display = ['name']

class ProductDetailInline(admin.TabularInline):
  model = ProductDetail
  #extra = 20

class ProductAttachmentInline(admin.TabularInline):
  model = ProductAttachment

class CategoryInline(admin.TabularInline):
  model = Category
  form = TreeModelInlineForm
  extra = 1

class CategoryAdmin(VisibleAdmin, MPTTModelAdmin, SortableModelAdmin):
  mptt_level_indent = 20
  list_display = ['name','shop']
  sortable = 'order'
  #inlines = [CategoryInline,]

  class Media:
    css = {
      'all' : ( '/static/redactor/redactor.css', )
    }
    js = (
      '/static/redactor/redactor.js',
      '/static/redactor/redactorlauncher.js',
      '/static/utils/suit-admin-csrf.js',
    )                
  

class ProductAdmin(VisibleAdmin):
  list_display = ('name', 'price', 'currency', 'measure_unit',)
  list_per_page = 20
  inlines = [
    ProductAttachmentInline,
    ProductDetailInline
  ]
  exclude = ('upc','text',)
  actions = [duplicate_product]
  list_filter = [ 'categories']
  search_fields = ['name']                                                                                                     

  class Media:
    css = {
      'all' : ( '/static/redactor/redactor.css', )
    }
    js = (
      '/static/redactor/redactor.js',
      '/static/redactor/redactorlauncher.js',
      '/static/utils/suit-admin-csrf.js',
    )                

class ProductCategoryFilterGroupItemInline(admin.TabularInline):
  model = ProductCategoryFilterGroupItem

class ProductCategoryFilterGroupAdmin(VisibleAdmin):
  inlines = [
    ProductCategoryFilterGroupItemInline
  ]

admin.site.register(MeasureUnit, MeasureUnitAdmin)
#admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategoryFilterGroup, ProductCategoryFilterGroupAdmin)
