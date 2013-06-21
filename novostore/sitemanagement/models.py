# coding=utf-8

from django.db import models
from django.db.models import Q,F

from django.core.validators import *

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop
from smart_selects.db_fields import ChainedForeignKey 
from photologue.models import ImageModel, Gallery, Photo
from django.utils.text import get_text_list, capfirst
from django.template.defaultfilters import slugify
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

class WebsiteMenu(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    text = models.CharField(max_length=80, db_index=True, verbose_name=_('Text'), help_text=_('Text inside the block'))
    url = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Url'), help_text=_('Url if block is hyperlink by itself'))
    order = models.PositiveIntegerField()

    class MPTTMeta:
        order_insertion_by = ['order']

    def save(self, *args, **kwargs):
        super(WebsiteMenu, self).save(*args, **kwargs)
        WebsiteMenu.objects.rebuild()


    def __unicode__(self):
        return unicode(self.text)

    class Meta:
        verbose_name = _("Website menu")
        verbose_name_plural = _("Website menu")