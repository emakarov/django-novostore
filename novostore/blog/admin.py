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
from django import forms

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_status')
    list_per_page = 20
    list_filter = ['user','terms']
    class Media:
        css = {
        	'all' : ( '/static/redactor/redactor.css', )
        }
        js = (
            '/static/redactor/redactor.js',
            '/static/redactor/redactorlauncher.js',
            #'/static/textredactor/textredactor.js',
        )                
#    inlines = [
#        ArticleCoverInline,
#    ]

class TermAdmin(admin.ModelAdmin):
    list_display = ('termname', 'termslug')
    search_fields = ['termname']

admin.site.register(Article,ArticleAdmin)
admin.site.register(Term,TermAdmin)
