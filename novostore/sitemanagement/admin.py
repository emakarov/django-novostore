# -*- coding: utf-8 -*-
""" 
Admin configuration for Site Management Tools
"""
from django.contrib import admin
from sitemanagement.models import *
from mptt.admin import MPTTModelAdmin
from suit.admin import SortableModelAdmin

class WebsiteMenuAdmin(MPTTModelAdmin, SortableModelAdmin):
    list_display = ['text','url']
    sortable = 'order'
    mptt_level_indent = 20

admin.site.register(WebsiteMenu,WebsiteMenuAdmin)