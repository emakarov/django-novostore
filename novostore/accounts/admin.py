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
from utils.visibility import VisibleAdmin
from accounts.models import AccountsUser
from utils.visibility import VisibleUserAdmin


class AccountsUserAdmin(VisibleUserAdmin):
  list_display = ['username']


admin.site.register(AccountsUser, AccountsUserAdmin)
