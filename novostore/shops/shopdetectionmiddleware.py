# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.conf import settings
from django.forms import widgets
from django.forms.extras.widgets import SelectDateWidget
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop
from django.db.models import Sum
from django.core.validators import *
from django.db.models import Q,F
from utils.visibility import VisibleManager
from shops import models as shop_models

class ShopDetectionMiddleware(object):
    def process_request(self, request):
        try:
            request.shop = shop_models.Shop.objects.get(domain = request.META['HTTP_HOST'])
        except:
            #request.shop = None
            try:
              request.shop = shop_models.Shop.objects.all()[0]
            except:
              request.shop = None