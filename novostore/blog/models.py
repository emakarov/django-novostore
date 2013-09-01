# coding=utf-8
from django.db import models
from django.db.models import Q,F
from django.contrib import auth
from django.core.validators import *
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop
from smart_selects.db_fields import ChainedForeignKey 
from photologue.models import ImageModel, Gallery, Photo
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

PUBLISH_STATUS_CHOICES = (('1',_('Draft')), ('2',_('Published')) ,) #need to be done 
ARTICLE_TYPES_CHOICES = (('1', _('Blog post')), ('2', _('Photo Gallery'))  ) 

class Term(models.Model):
    termname = models.CharField(_("Term name"), max_length=255, blank=True, default='', help_text = _("Term name"))
    termslug = models.CharField(_("Term slug"), max_length=255, blank=True, default='', help_text = _("Term slug"))
    is_servicecat = models.BooleanField("Service category feature", help_text = "Service category feature")
    
    def __unicode__(self):
        return self.termname

    def articles_count(self):
        return len(Article.objects.filter(terms=self, publish_status = '2').exclude(cover=None))

    class Meta:
        verbose_name = _("Blog term")
        verbose_name_plural = _("Blog terms")

# Create your models here.
class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=_('Author'),help_text=_('Author'))
    title = models.CharField(_("Title"), max_length=255, help_text = "title")
    description =  models.TextField(_("Description"),  blank=True, default='', help_text = _("Description"))
    terms = models.ManyToManyField(Term,verbose_name=_("Terms"),blank=True)
    text = models.TextField(_("Text"),blank=True)
    publish_status = models.CharField(max_length=1, choices=PUBLISH_STATUS_CHOICES)
    publish_date = models.DateTimeField(blank=True,null=True)
    article_type = models.CharField(max_length=1, choices=ARTICLE_TYPES_CHOICES)
    gallery = models.ForeignKey(Gallery, null=True, blank=True,verbose_name=_("Gallery"))
    cover = ChainedForeignKey(
        Photo,
        chained_field="gallery",
        chained_model_field="galleries", 
        show_all=False, 
        auto_choose=True,
        verbose_name=_("Cover"), 
        null=True, blank=True
    )
    longitude = models.DecimalField(max_digits=11,decimal_places=7, verbose_name=_("Longitude"),
            validators=[MinValueValidator(-180),MaxValueValidator(180)],null=True, blank=True)

    latitude = models.DecimalField(max_digits=11,decimal_places=7, verbose_name=_("Latitude"),
            validators=[MinValueValidator(-90),MaxValueValidator(90)],null=True, blank=True)
    template = models.CharField(max_length=100, choices=settings.BLOG_TEMPLATES)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("Blog article")
        verbose_name_plural = _("Blog articles")
        ordering = ['-id']