from models import *
from django.contrib import admin
from utils.visibility import VisibleAdmin

class LeadAdmin(admin.ModelAdmin):
  list_display = ['shop','received','content']

admin.site.register(Lead,LeadAdmin)