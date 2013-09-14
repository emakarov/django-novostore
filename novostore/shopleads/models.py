from django.db import models
from django.db.models import Q,F
#from django.contrib import auth

from django.core.validators import *

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop
#from util.base_models import *
from smart_selects.db_fields import ChainedForeignKey 
from photologue.models import ImageModel, Gallery, Photo
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.contrib.comments.models import Comment
from utils.visibility import VisibleManager, VisibleTreeManager
from django.conf import settings

class Lead(models.Model):
  shop = models.ForeignKey('shops.Shop',verbose_name = _("Shop"), related_name='leads')
  content = models.TextField(blank=True, default='', verbose_name=_('Content'), help_text=_('content'))
  received = models.DateTimeField(verbose_name=_("Received"), blank=True, null=True, auto_now_add = True)

  #objects = VisibleManager(Q(shop__owner=lambda r:r.user))
            
  def __unicode__(self):
    return self.shop.name
  
  class Meta:
    verbose_name = _("Lead")
    verbose_name_plural = _("Leads")
