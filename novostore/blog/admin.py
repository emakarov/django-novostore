# -*- coding: utf-8 -*-
""" 
Admin configuration for Blog
"""
from django import template
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop
from django.contrib.admin.util import model_ngettext
from django.contrib.admin import helpers
from django.contrib import messages
from django.utils.datastructures import SortedDict
from django.shortcuts import render_to_response
from django.utils.encoding import force_unicode
from django.contrib import admin
from models import *
#from util import base_admin as util_admin
from django.forms import ModelForm

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_status')
    list_per_page = 20
    list_filter = ['user','terms']
#    class Media:
#        js = [
#            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
#            '/static/grappelli/tinymce_setup/tinymce_setup.js',
#        ]                
#    inlines = [
#        ArticleCoverInline,
#    ]

class TermAdmin(admin.ModelAdmin):
    list_display = ('termname', 'termslug')
    search_fields = ['termname']

admin.site.register(Article,ArticleAdmin)
admin.site.register(Term,TermAdmin)
