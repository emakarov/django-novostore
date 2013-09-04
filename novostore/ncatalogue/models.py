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
from shops import models as shop_models
from utils.visibility import VisibleManager, VisibleTreeManager

#from commerce import models as commerce_models
# Create your models here.

class MeasureUnit(models.Model):
  name = models.CharField(_("Name"),max_length=50)
  shortname = models.CharField(_("Short name"),max_length=50)
  per_name = models.CharField(_("Per name"),max_length=50)
  name_international = models.CharField(_("Name international"),max_length=50,blank=True,null=True)
  shortname_international = models.CharField(_("Short name international"),max_length=50,blank=True,null=True)
  per_name_international = models.CharField(_("Per name internationl"),max_length=50,blank=True,null=True)
  description = models.TextField(blank=True, default='', verbose_name=_('Description'), help_text=_('Details of this measure unit'))
  
  def __unicode__(self):
    return "%s" % (self.shortname)
  
  class Meta:
    verbose_name = _("Measure Unit")
    verbose_name_plural = _("Measure Units")

class Category(MPTTModel):
  name = models.CharField(_("Category name"), max_length=255, blank=True, default='', help_text = _("Term name"), db_index=True)
  slug = models.SlugField(_('Slug'), max_length=128, unique=True, db_index=True)
  is_operating = models.BooleanField(_("Operating status"), help_text = _("Service category status"), default=True)
  # Some product type don't require shipping (eg digital products) - we use
  # this field to take some shortcuts in the checkout.
  requires_shipping = models.BooleanField(_("Requires shipping?"), default=True)
  parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children')
  order = models.PositiveIntegerField()
  shop = models.ForeignKey(shop_models.Shop,verbose_name = _("Shop"),related_name='categories')
  photo = models.ForeignKey(Photo, null=True, blank=True,verbose_name=_("Photo"))
  description =  models.CharField(_("Description"), max_length=255, blank=True, default='', help_text = _("Description"),db_index=True)


  objects = VisibleTreeManager(Q(shop__owner=lambda r:r.user))
    
  class MPTTMeta:
        order_insertion_by = ['order']
        
  # It is required to rebuild tree after save, when using order for mptt-tree
  def save(self, *args, **kwargs):
    super(Category, self).save(*args, **kwargs)
    Category.objects.rebuild()
            
  def __unicode__(self):
    return self.name
  
  class Meta:
    verbose_name = _("Category")
    verbose_name_plural = _("Categories")
    
class Product(models.Model):
  from commerce.models import Currency 
  # Universal product code
  upc = models.CharField(_("UPC"), max_length=64, blank=True, null=True,
        help_text=_("Universal Product Code (UPC) is an identifier for "
                    "a product which is not specific to a particular "
                    " supplier. Eg an ISBN for a book."))    
  gallery = models.ForeignKey(Gallery, null=True, blank=True,verbose_name=_("Gallery"))
  cover = ChainedForeignKey(
        Photo,
        chained_field="gallery",
        chained_model_field="galleries", 
        show_all=False, 
        auto_choose=True,
        verbose_name=_("Main photo"), 
        null=True, blank=True
  )
  name = models.CharField(_("Name"), max_length=255, help_text = "name", db_index=True)
  description =  models.CharField(_("Description"), max_length=255, blank=True, default='', help_text = _("Description"),db_index=True)
  long_description = models.TextField(blank=True, default='', verbose_name=_('Long description'), help_text=_('Long description'))
  categories = models.ManyToManyField(Category,verbose_name=_("Categories"),blank=True)
  text = models.TextField(_("Text"),blank=True,null=True)
  price = models.FloatField(_("Base Price"),blank=True,null=True,help_text=_("Base price"))
  currency = models.ForeignKey(Currency)
  measure_unit = models.ForeignKey(MeasureUnit)
  
  if settings.SINGLE_SHOP is not None:
    if not settings.SINGLE_SHOP:
      objects = VisibleManager(categories__shop__owner=lambda r:r.user)

  def __unicode__(self):
    return "%s : %s" % (self.name, self.upc)
  
  class Meta:
    verbose_name = _("Product")
    verbose_name_plural = _("Products")

class ProductAttachment(models.Model):
  name = models.CharField(_("File name"), max_length=255, blank=True, default='', help_text = _("File name"), db_index=True)
  file = models.FileField(_("File"), upload_to="attachments/")
  product = models.ForeignKey(Product,verbose_name=_("Product"), related_name="attachments")

  def __unicode__(self):
    return self.name
  
  class Meta:
    verbose_name = _("Product Attachment")
    verbose_name_plural = _("Product Attachments")

class ProductDetail(models.Model):
  name = models.CharField(_("Name"), max_length=255, blank=True, default='', help_text = _("Detail name"), db_index=True)
  value = models.CharField(_("Value"), max_length=255, blank=True, default='', help_text = _("Value"), db_index=True)
  product = models.ForeignKey(Product,verbose_name=_("Product"), related_name="details")

  def __unicode__(self):
    return self.name
  
  class Meta:
    verbose_name = _("Product Detail")
    verbose_name_plural = _("Product Details")
  
  

#Use of django comments framework to support ratings
#class ProductComment(Comment):
#    title = models.CharField(_("Product Comment"), max_length=300)
#    stars = models.IntegerField(_("Stars"), default = 1)
#    categories = models.ManyToManyField(Category,verbose_name=_("Categories"),blank=True, null=True)
    
#    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
#        return ProductComment

#    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the title field
#        data = super(CommentFormWithTitle, self).get_comment_create_data()
#        data['title'] = self.cleaned_data['title']
#        return data
